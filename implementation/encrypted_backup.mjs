import { createCipheriv, createDecipheriv, createHash, randomBytes, scryptSync } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";

function fail(message) { process.stderr.write(JSON.stringify({ state: "HELD", error: message }) + "\n"); process.exit(2); }
function options() { const out={}; for(let i=3;i<process.argv.length;i+=2){const key=process.argv[i];if(!key?.startsWith("--")||i+1>=process.argv.length)fail("invalid arguments");out[key.slice(2)]=process.argv[i+1];}return out; }
function passphrase(){const value=readFileSync(0).toString("utf8").replace(/[\r\n]+$/,"");if(Buffer.byteLength(value,"utf8")<16)fail("passphrase must contain at least 16 UTF-8 bytes");return value;}
function noOverwrite(path){if(existsSync(path))fail(`target already exists: ${path}`);}
function sha(body){return createHash("sha256").update(body).digest("hex");}
const SCRYPT={name:"scrypt",N:32768,r:8,p:1,key_bytes:32};
function derive(secret,salt){return scryptSync(secret,salt,SCRYPT.key_bytes,{N:SCRYPT.N,r:SCRYPT.r,p:SCRYPT.p,maxmem:64*1024*1024});}

const command=process.argv[2], option=options();
if(command==="encrypt"){
  if(!option.input||!option.output)fail("encrypt requires --input and --output");noOverwrite(option.output);
  const secret=passphrase(), plaintext=readFileSync(option.input), salt=randomBytes(16), nonce=randomBytes(12);
  const header={schema:"hirc.encrypted-backup/1",cipher:"AES-256-GCM",kdf:SCRYPT,salt_base64:salt.toString("base64"),nonce_base64:nonce.toString("base64"),plaintext_sha256:sha(plaintext),plaintext_bytes:plaintext.length};
  const aad=Buffer.from(JSON.stringify(header));const cipher=createCipheriv("aes-256-gcm",derive(secret,salt),nonce);cipher.setAAD(aad);const ciphertext=Buffer.concat([cipher.update(plaintext),cipher.final()]);const envelope={...header,ciphertext_base64:ciphertext.toString("base64"),tag_base64:cipher.getAuthTag().toString("base64")};
  writeFileSync(option.output,JSON.stringify(envelope,null,2)+"\n",{mode:0o600,flag:"wx"});process.stdout.write(JSON.stringify({schema:"hirc.encrypted-backup-result/1",operation:"encrypt",path:option.output,encrypted_bytes:ciphertext.length,plaintext_sha256:header.plaintext_sha256,key_stored:false})+"\n");
}else if(command==="decrypt"){
  if(!option.input||!option.output)fail("decrypt requires --input and --output");noOverwrite(option.output);const secret=passphrase();let envelope;try{envelope=JSON.parse(readFileSync(option.input,"utf8"));}catch{fail("encrypted backup unreadable");}
  const {ciphertext_base64,tag_base64,...header}=envelope;if(header.schema!=="hirc.encrypted-backup/1"||header.cipher!=="AES-256-GCM"||JSON.stringify(header.kdf)!==JSON.stringify(SCRYPT))fail("encrypted backup parameters unsupported");
  try{const salt=Buffer.from(header.salt_base64,"base64"),nonce=Buffer.from(header.nonce_base64,"base64"),aad=Buffer.from(JSON.stringify(header)),decipher=createDecipheriv("aes-256-gcm",derive(secret,salt),nonce);decipher.setAAD(aad);decipher.setAuthTag(Buffer.from(tag_base64,"base64"));const plaintext=Buffer.concat([decipher.update(Buffer.from(ciphertext_base64,"base64")),decipher.final()]);if(plaintext.length!==header.plaintext_bytes||sha(plaintext)!==header.plaintext_sha256)fail("decrypted backup identity mismatch");writeFileSync(option.output,plaintext,{mode:0o600,flag:"wx"});process.stdout.write(JSON.stringify({schema:"hirc.encrypted-backup-result/1",operation:"decrypt",path:option.output,plaintext_bytes:plaintext.length,plaintext_sha256:sha(plaintext),key_stored:false})+"\n");}catch(error){fail("encrypted backup authentication failed");}
}else fail("command must be encrypt or decrypt");
