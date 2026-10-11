import { createHash, createPrivateKey, createPublicKey, generateKeyPairSync, sign, verify } from "node:crypto";
import { chmodSync, existsSync, readFileSync, writeFileSync } from "node:fs";

function fail(message) { process.stderr.write(JSON.stringify({ state: "HELD", error: message }) + "\n"); process.exit(2); }
function args() { const out = {}; for (let i = 3; i < process.argv.length; i += 2) { const key = process.argv[i]; if (!key?.startsWith("--") || i + 1 >= process.argv.length) fail("invalid arguments"); out[key.slice(2)] = process.argv[i + 1]; } return out; }
function passphrase() { const value = readFileSync(0); const clean = value.toString("utf8").replace(/[\r\n]+$/, ""); if (Buffer.byteLength(clean, "utf8") < 16) fail("passphrase must contain at least 16 UTF-8 bytes"); return clean; }
function noOverwrite(path) { if (existsSync(path)) fail(`target already exists: ${path}`); }
function fingerprint(publicKey) { const der = publicKey.export({ type: "spki", format: "der" }); return createHash("sha256").update(der).digest("hex"); }

const command = process.argv[2];
const option = args();
if (command === "generate") {
  if (!option.private || !option.public) fail("generate requires --private and --public");
  noOverwrite(option.private); noOverwrite(option.public);
  const secret = passphrase();
  const pair = generateKeyPairSync("ed25519");
  const privatePem = pair.privateKey.export({ type: "pkcs8", format: "pem", cipher: "aes-256-cbc", passphrase: secret });
  const publicPem = pair.publicKey.export({ type: "spki", format: "pem" });
  writeFileSync(option.private, privatePem, { mode: 0o600, flag: "wx" });
  writeFileSync(option.public, publicPem, { mode: 0o644, flag: "wx" });
  try { chmodSync(option.private, 0o600); } catch {}
  process.stdout.write(JSON.stringify({ schema: "hirc.release-key/1", algorithm: "Ed25519", public_key_fingerprint_sha256: fingerprint(pair.publicKey), private_key_encrypted: true, private_key_path: option.private, public_key_path: option.public }) + "\n");
} else if (command === "sign") {
  if (!option.private || !option.manifest || !option.output) fail("sign requires --private, --manifest and --output");
  noOverwrite(option.output);
  const secret = passphrase();
  const manifest = readFileSync(option.manifest);
  let privateKey; try { privateKey = createPrivateKey({ key: readFileSync(option.private), format: "pem", passphrase: secret }); } catch { fail("private key or passphrase invalid"); }
  const publicKey = createPublicKey(privateKey);
  const signature = sign(null, manifest, privateKey);
  const envelope = { schema: "hirc.release-signature/1", algorithm: "Ed25519", manifest_sha256: createHash("sha256").update(manifest).digest("hex"), public_key_fingerprint_sha256: fingerprint(publicKey), signature_base64: signature.toString("base64") };
  writeFileSync(option.output, JSON.stringify(envelope, null, 2) + "\n", { mode: 0o644, flag: "wx" });
  process.stdout.write(JSON.stringify(envelope) + "\n");
} else if (command === "verify") {
  if (!option.public || !option.manifest || !option.signature) fail("verify requires --public, --manifest and --signature");
  const manifest = readFileSync(option.manifest);
  let envelope; try { envelope = JSON.parse(readFileSync(option.signature, "utf8")); } catch { fail("signature envelope unreadable"); }
  const publicKey = createPublicKey(readFileSync(option.public));
  const digest = createHash("sha256").update(manifest).digest("hex");
  const valid = envelope.schema === "hirc.release-signature/1" && envelope.algorithm === "Ed25519" && envelope.manifest_sha256 === digest && envelope.public_key_fingerprint_sha256 === fingerprint(publicKey) && verify(null, manifest, publicKey, Buffer.from(envelope.signature_base64 || "", "base64"));
  if (!valid) fail("release signature verification failed");
  process.stdout.write(JSON.stringify({ schema: "hirc.release-signature-verification/1", valid: true, manifest_sha256: digest, public_key_fingerprint_sha256: fingerprint(publicKey) }) + "\n");
} else fail("command must be generate, sign or verify");
