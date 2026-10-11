$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$schemaPath = Join-Path $root 'review\contracts\hirc-bridge-gate.candidate.schema.json'
$fixturePath = Join-Path $root 'review\fixtures\security-bridge-stage-cases-v1.json'
$stage6Path = Join-Path $root 'review\contracts\fixtures\valid-bridge-stage6-entry.json'
$outputPath = Join-Path $root 'review\fixtures\security-bridge-stage-validation-v1.json'
$fixture = Get-Content -Raw $fixturePath | ConvertFrom-Json
$stage6 = Get-Content -Raw $stage6Path | ConvertFrom-Json

function Copy-Record($record) { return ($record | ConvertTo-Json -Depth 50 | ConvertFrom-Json) }
function Test-Structural($record) { return (Test-Json -Json ($record | ConvertTo-Json -Depth 50) -SchemaFile $schemaPath -ErrorAction SilentlyContinue) }

function Test-StageSemantic($record) {
    $names = @('stage1','stage2','stage3','stage4','stage5','stage6','stage7')
    $map = @{
        STAGE1_SPEC = 0; STAGE2_OFFLINE = 1; STAGE3_TWO_SYSTEM_LAB = 2;
        STAGE4_HOSTILE_LAB = 3; STAGE5_INDEPENDENT_ASSESSMENT = 4;
        STAGE6_BOUNDED_PILOT = 5; STAGE7_BROADER_ACTIVATION = 6
    }
    $reasons = @()
    if ($record.current_stage -eq 'HELD') {
        $heldIndexes = @()
        for ($i=0; $i -lt $names.Count; $i++) {
            if ($record.stages.($names[$i]).state -eq 'HELD') { $heldIndexes += $i }
        }
        if ($heldIndexes.Count -ne 1) { $reasons += 'HELD must identify exactly one held stage' }
        if ($heldIndexes.Count -eq 1) {
            $held = $heldIndexes[0]
            for ($i=0; $i -lt $held; $i++) { if ($record.stages.($names[$i]).state -ne 'PASS') { $reasons += "prior $($names[$i]) is not PASS" } }
            for ($i=$held+1; $i -lt $names.Count; $i++) { if ($record.stages.($names[$i]).state -ne 'NOT_STARTED') { $reasons += "future $($names[$i]) advanced after HELD" } }
        }
    } else {
        $current = $map[$record.current_stage]
        for ($i=0; $i -lt $current; $i++) { if ($record.stages.($names[$i]).state -ne 'PASS') { $reasons += "prior $($names[$i]) is not PASS" } }
        for ($i=$current+1; $i -lt $names.Count; $i++) { if ($record.stages.($names[$i]).state -ne 'NOT_STARTED') { $reasons += "future $($names[$i]) advanced" } }
    }
    return [pscustomobject]@{ valid = ($reasons.Count -eq 0); reasons = $reasons }
}

$positives = foreach ($item in @(
    [pscustomobject]@{name='early_held'; record=$fixture.early_held},
    [pscustomobject]@{name='stage6_entry'; record=$stage6},
    [pscustomobject]@{name='stage7_decision'; record=$fixture.stage7_decision}
)) {
    $semantic = Test-StageSemantic $item.record
    [pscustomobject]@{name=$item.name; structural=(Test-Structural $item.record); semantic=$semantic.valid; reasons=$semantic.reasons; accepted=((Test-Structural $item.record) -and $semantic.valid)}
}

$cases = @()
function Add-Adverse($name, $record, $expectedLayer) {
    $structural = Test-Structural $record
    $semantic = Test-StageSemantic $record
    $script:cases += [pscustomobject]@{name=$name; expected_layer=$expectedLayer; structural=$structural; semantic=$semantic.valid; reasons=$semantic.reasons; rejected=(-not ($structural -and $semantic.valid))}
}

$record = Copy-Record $fixture.stage7_decision; $record.stages.stage1.evidence_refs=@(); Add-Adverse 'pass_without_evidence' $record 'schema'
$record = Copy-Record $fixture.stage7_decision; $record.current_stage='STAGE3_TWO_SYSTEM_LAB'; $record.stages.stage2.state='NOT_STARTED'; $record.stages.stage3.state='IN_PROGRESS'; $record.stages.stage4.state='NOT_STARTED'; $record.stages.stage5.state='NOT_STARTED'; $record.stages.stage6.state='NOT_STARTED'; $record.stages.stage6.evidence_refs=@(); $record.stages.stage6.PSObject.Properties.Remove('entry_authorization_ref'); $record.stages.stage6.PSObject.Properties.Remove('stop_conditions_ref'); $record.stages.stage7.state='NOT_STARTED'; $record.stages.stage7.evidence_refs=@(); $record.stages.stage7.PSObject.Properties.Remove('decision_ref'); Add-Adverse 'missing_prior_stage' $record 'semantic'
$record = Copy-Record $stage6; $record.stages.stage6.PSObject.Properties.Remove('entry_authorization_ref'); Add-Adverse 'stage6_without_authority' $record 'schema'
$record = Copy-Record $fixture.stage7_decision; $record.stages.stage6.state='NOT_STARTED'; $record.stages.stage6.evidence_refs=@(); Add-Adverse 'stage7_without_stage6_pass' $record 'schema-or-semantic'
$record = Copy-Record $fixture.stage7_decision; $record.current_stage='HELD'; $record.stages.stage5.state='HELD'; Add-Adverse 'held_hides_later_activation' $record 'semantic'

$state = if (($positives | Where-Object { -not $_.accepted }).Count -eq 0 -and ($cases | Where-Object { -not $_.rejected }).Count -eq 0) { 'PASS' } else { 'FAIL' }
$result = [pscustomobject]@{
    schema='hirc.security-bridge-stage-validation/1'; state=$state;
    target=[pscustomobject]@{path='review/contracts/hirc-bridge-gate.candidate.schema.json';sha256=(Get-FileHash $schemaPath -Algorithm SHA256).Hash.ToLower()};
    fixture=[pscustomobject]@{path='review/fixtures/security-bridge-stage-cases-v1.json';sha256=(Get-FileHash $fixturePath -Algorithm SHA256).Hash.ToLower()};
    positives=$positives; adverse=$cases;
    nonclaim='Schema plus deterministic stage-order validation only; not implementation, protocol security, independent assessment or Bridge activation.'
}
$rendered=$result|ConvertTo-Json -Depth 12
[IO.File]::WriteAllText($outputPath,$rendered+"`n",[Text.UTF8Encoding]::new($false))
$rendered
if($state-ne'PASS'){exit 1}
