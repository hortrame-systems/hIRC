$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$schemaPath = Join-Path $root 'review\contracts\hirc-request-case.candidate.schema.v2.json'
$fixturePath = Join-Path $root 'review\fixtures\security-request-state-cases-v1.json'
$outputPath = Join-Path $root 'review\fixtures\security-request-state-validation-v1.json'
$fixture = Get-Content -Raw $fixturePath | ConvertFrom-Json
$waymarkFixturePath = Join-Path $root 'review\fixtures\waymark-trust-contract-cases-v1.json'
$waymarkFixture = Get-Content -Raw $waymarkFixturePath | ConvertFrom-Json

function Copy-Record($record) {
    return ($record | ConvertTo-Json -Depth 50 | ConvertFrom-Json)
}

function Test-Record($record) {
    $json = $record | ConvertTo-Json -Depth 50
    return (Test-Json -Json $json -SchemaFile $schemaPath -ErrorAction SilentlyContinue)
}
function Get-PrivacySha($privacy) {
    $ordered = [ordered]@{data_classes=@($privacy.data_classes);audience_refs=@($privacy.audience_refs);purpose_ref=$privacy.purpose_ref;consent_snapshot_ref=$privacy.consent_snapshot_ref;consent_current=[bool]$privacy.consent_current;retention_policy_ref=$privacy.retention_policy_ref;derived_data_policy_ref=$privacy.derived_data_policy_ref;egress_policy_ref=$privacy.egress_policy_ref;deletion_residual_ref=$privacy.deletion_residual_ref;encryption_required=[bool]$privacy.encryption_required}
    $text = $ordered | ConvertTo-Json -Compress
    $algorithm=[Security.Cryptography.SHA256]::Create();try{return [Convert]::ToHexString($algorithm.ComputeHash([Text.Encoding]::UTF8.GetBytes($text))).ToLower()}finally{$algorithm.Dispose()}
}

function Test-PrivacySnapshot($record) {
    if ($null -eq $record.effect) { return $true }
    return $record.effect.privacy_snapshot_sha256 -eq (Get-PrivacySha $record.privacy)
}

function Set-PathValue($record, $path, $value) {
    $cursor = $record
    for ($index = 0; $index -lt $path.Count - 1; $index++) {
        $cursor = $cursor.($path[$index])
    }
    $cursor.($path[-1]) = $value
}

function Convert-WaymarkRequest($record) {
    $record.schema_version = 'hirc.request-case/2-candidate'
    $record.source | Add-Member -NotePropertyName admission_state -NotePropertyValue 'ADMITTED_BEFORE_CASE_CREATION'
    $record.source | Add-Member -NotePropertyName admission_ref -NotePropertyValue 'synthetic:privacy-admission'
    foreach ($interpretation in $record.interpretations) {
        $value = [double]$interpretation.confidence
        $interpretation.confidence = [pscustomobject]@{
            state = 'ESTIMATED'
            value = $value
            method_ref = 'synthetic:declared-estimate'
            uncertainty_ref = 'synthetic:estimate-limits'
        }
    }
    $record.low_consequence | Add-Member -NotePropertyName profile_ref -NotePropertyValue 'profile:isolated-personal-theme'
    $record.low_consequence | Add-Member -NotePropertyName profile_version -NotePropertyValue '1'
    $record.low_consequence | Add-Member -NotePropertyName current_permission_rechecked -NotePropertyValue $true
    $record.low_consequence | Add-Member -NotePropertyName changed_material_premises -NotePropertyValue $false
    $record | Add-Member -NotePropertyName privacy -NotePropertyValue ([pscustomobject]@{
        data_classes = @('data:synthetic-request')
        audience_refs = @('audience:owner')
        purpose_ref = 'purpose:synthetic-theme'
        consent_snapshot_ref = 'consent:synthetic-current'
        consent_current = $true
        retention_policy_ref = 'retention:synthetic-short'
        derived_data_policy_ref = 'derived:inherit'
        egress_policy_ref = 'egress:none'
        deletion_residual_ref = 'residual:none'
        encryption_required = $false
    })
    return $record
}

$positive = foreach ($name in @('analysis','performed','declined')) {
    $record = Copy-Record $fixture.bases.$name
    [pscustomobject]@{ name = $name; accepted = ((Test-Record $record) -and (Test-PrivacySnapshot $record)) }
}

$cases = @()
function Add-Adverse($name, $record, $expected) {
    $script:cases += [pscustomobject]@{
        name = $name
        expected = $expected
        rejected = -not ((Test-Record $record) -and (Test-PrivacySnapshot $record))
    }
}

$record = Copy-Record $fixture.bases.performed
$record.authority.current = $false
Add-Adverse 'proceed_with_stale_authority' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.participation.state = 'DECLINED'
Add-Adverse 'proceed_with_declined_participation' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.PSObject.Properties.Remove('effect')
Add-Adverse 'performed_without_effect' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.effect.requested = $false
Add-Adverse 'sent_without_request' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.effect.sent = 'NO'
$record.effect.provider_accepted = 'YES'
Add-Adverse 'provider_accepted_without_send' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.effect.sent = 'UNKNOWN'
$record.effect.observed = 'YES'
Add-Adverse 'observed_without_send' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.effect.PSObject.Properties.Remove('preview_sha256')
Add-Adverse 'effect_without_preview_binding' $record 'schema rejection'

$record = Copy-Record $fixture.bases.performed
$record.privacy.audience_refs += 'audience:external'
Add-Adverse 'effect_privacy_snapshot_audience_widened' $record 'semantic rejection'

$record = Copy-Record $fixture.bases.performed
$record.privacy.purpose_ref = 'purpose:other'
Add-Adverse 'effect_privacy_snapshot_purpose_changed' $record 'semantic rejection'

$record = Copy-Record $fixture.bases.performed
$second = Copy-Record $record.interpretations[0]
$second.interpretation_id = 'interpretation:extra'
$record.interpretations = @($record.interpretations[0], $second)
Add-Adverse 'two_selected_interpretations' $record 'schema rejection'

$record = Copy-Record $fixture.bases.declined
$record.action_disposition.state = 'PROCEED'
$record.action_disposition.effect_gate_state = 'PASS'
Add-Adverse 'declined_state_proceeds' $record 'schema rejection'

$waymarkRegression = foreach ($case in @($waymarkFixture.cases | Where-Object { $_.base -eq 'request' })) {
    $record = Copy-Record $waymarkFixture.bases.request
    foreach ($patch in $case.patches) {
        Set-PathValue $record @($patch.path) $patch.value
    }
    $record = Convert-WaymarkRequest $record
    $accepted = Test-Record $record
    $expected = $case.id -eq 'WST-C01'
    [pscustomobject]@{
        id = $case.id
        expected_accepted = $expected
        accepted = $accepted
        pass = ($accepted -eq $expected)
    }
}

$state = if (($positive | Where-Object { -not $_.accepted }).Count -eq 0 -and ($cases | Where-Object { -not $_.rejected }).Count -eq 0 -and ($waymarkRegression | Where-Object { -not $_.pass }).Count -eq 0) { 'PASS' } else { 'FAIL' }
$result = [pscustomobject]@{
    schema = 'hirc.security-request-state-validation/1'
    state = $state
    target = [pscustomobject]@{
        path = 'review/contracts/hirc-request-case.candidate.schema.v2.json'
        sha256 = (Get-FileHash -LiteralPath $schemaPath -Algorithm SHA256).Hash.ToLower()
    }
    fixture = [pscustomobject]@{
        path = 'review/fixtures/security-request-state-cases-v1.json'
        sha256 = (Get-FileHash -LiteralPath $fixturePath -Algorithm SHA256).Hash.ToLower()
    }
    positive = $positive
    adverse = $cases
    waymark_request_regression = $waymarkRegression
    nonclaim = 'Schema-level request-state invariants only; not authority truth, runtime dispatch, privacy/dataflow closure, independent security review or S014 acceptance.'
}
$rendered = $result | ConvertTo-Json -Depth 12
[IO.File]::WriteAllText($outputPath, $rendered + "`n", [Text.UTF8Encoding]::new($false))
$rendered
if ($state -ne 'PASS') { exit 1 }
