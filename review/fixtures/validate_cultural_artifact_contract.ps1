$ErrorActionPreference = 'Stop'

$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$schemaPath = Join-Path $root 'review\contracts\hirc-cultural-artifact.candidate.schema.json'
$fixturePath = Join-Path $root 'review\fixtures\cultural-artifact-contract-cases-v1.json'
$resultPath = Join-Path $root 'review\fixtures\cultural-artifact-contract-validation-v1.json'
$fixtures = Get-Content -LiteralPath $fixturePath -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100

function Copy-Object($value) {
    return (ConvertFrom-Json -InputObject (ConvertTo-Json -InputObject $value -Depth 100 -Compress) -Depth 100)
}

function Set-ObjectPath($target, $patch) {
    [string]$path = $patch.path
    $parts = $path.Split('.')
    $current = $target
    for ($index = 0; $index -lt $parts.Count - 1; $index++) {
        $current = $current.($parts[$index])
        if ($null -eq $current) { throw "missing patch parent: $path" }
    }
    $name = $parts[$parts.Count - 1]
    $rawValue = $patch.PSObject.Properties['value'].Value
    $jsonValue = ConvertTo-Json -InputObject $rawValue -Depth 100 -Compress
    $copy = ConvertFrom-Json -InputObject $jsonValue -Depth 100 -NoEnumerate
    $current | Add-Member -NotePropertyName $name -NotePropertyValue $copy -Force
}

function Remove-ObjectPath($target, [string]$path) {
    $parts = $path.Split('.')
    $current = $target
    for ($index = 0; $index -lt $parts.Count - 1; $index++) {
        $current = $current.($parts[$index])
        if ($null -eq $current) { throw "missing delete parent: $path" }
    }
    $name = [string]$parts[$parts.Count - 1]
    $current.PSObject.Properties.Remove($name)
    if ($null -ne $current.PSObject.Properties[$name]) { throw "delete failed: $path" }
}

function Test-Semantics($payload) {
    $errors = [System.Collections.Generic.List[string]]::new()
    $events = @($payload.provenance)
    if ($events.Count -lt 1 -or $events[0].event_type -ne 'CREATED') { $errors.Add('created-provenance') }
    if ($events[-1].output_sha256 -ne $payload.content_ref.content_sha256) { $errors.Add('current-content-lineage') }
    if (@($events | Where-Object event_type -eq 'DISSENT_RECORDED').Count -gt 0 -and @($payload.dissent).Count -eq 0) {
        $errors.Add('dissent-erasure')
    }
    foreach ($item in @($payload.dissent)) {
        if ($item.preserved -ne $true) { $errors.Add('dissent-not-preserved') }
    }
    if ($payload.state -eq 'CORRECTED') {
        if ($null -eq $payload.correction -or $payload.correction.preserves_predecessor -ne $true) { $errors.Add('destructive-correction') }
        elseif ($payload.correction.correction_sha256 -ne $payload.content_ref.content_sha256) { $errors.Add('correction-output-mismatch') }
        elseif (@($events | Where-Object event_type -eq 'CORRECTED').Count -lt 1) { $errors.Add('correction-provenance') }
        elseif ($payload.correction.predecessor_sha256 -notin @($events.input_sha256_refs)) { $errors.Add('correction-predecessor-lineage') }
    }
    if ($payload.state -eq 'SUPERSEDED' -and ($null -eq $payload.supersession -or $payload.supersession.predecessor_recoverable -ne $true)) {
        $errors.Add('destructive-supersession')
    }
    if (@($payload.related_contexts | Where-Object inheritance_authorized -eq $true).Count -gt 0) { $errors.Add('context-inheritance') }
    if ($payload.authority_effect -ne 'NONE') { $errors.Add('authority-effect') }
    if ($payload.cultural_score_effect -ne 'NONE') { $errors.Add('cultural-score-effect') }
    if ($payload.content_ref.body_in_record -ne $false) { $errors.Add('body-in-record') }
    foreach ($audience in @($payload.permissions.allowed_audience_refs)) {
        if ($audience -notin @($payload.context.audience_refs)) { $errors.Add('audience-expansion') }
    }
    return @($errors | Sort-Object -Unique)
}

$rows = @()
foreach ($case in $fixtures.cases) {
    $payload = Copy-Object $fixtures.base
    foreach ($patch in @($case.patches)) {
        if ($patch.op -eq 'set') { Set-ObjectPath $payload $patch }
        elseif ($patch.op -eq 'delete') { Remove-ObjectPath $payload $patch.path }
        else { throw "unsupported patch operation: $($patch.op)" }
    }
    $json = $payload | ConvertTo-Json -Depth 100
    $structuralErrors = @()
    $structuralAccepted = Test-Json -Json $json -SchemaFile $schemaPath -ErrorAction SilentlyContinue -ErrorVariable structuralErrors
    $semanticErrors = if ($structuralAccepted) { @(Test-Semantics $payload) } else { @() }
    $semanticState = if (-not $structuralAccepted) { 'NOT_RUN' } elseif ($semanticErrors.Count -eq 0) { 'ACCEPT' } else { 'REJECT' }
    $structuralState = if ($structuralAccepted) { 'ACCEPT' } else { 'REJECT' }
    $rows += [ordered]@{
        name = $case.name
        expected_structural = $case.expected_structural
        actual_structural = $structuralState
        expected_semantic = $case.expected_semantic
        actual_semantic = $semanticState
        structural_error_count = @($structuralErrors).Count
        structural_errors = @($structuralErrors | ForEach-Object { $_.ToString() })
        semantic_errors = @($semanticErrors)
        pass = $structuralState -eq $case.expected_structural -and $semanticState -eq $case.expected_semantic
    }
}

$schemaHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $schemaPath).Hash.ToLower()
$fixtureHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $fixturePath).Hash.ToLower()
$scriptHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToLower()
$result = [ordered]@{
    schema = 'hirc.cultural-artifact-contract-validation/1'
    stone = 'M03-S007'
    schema_binding = [ordered]@{path='review/contracts/hirc-cultural-artifact.candidate.schema.json';sha256=$schemaHash}
    fixture_binding = [ordered]@{path='review/fixtures/cultural-artifact-contract-cases-v1.json';sha256=$fixtureHash}
    harness_binding = [ordered]@{path='review/fixtures/validate_cultural_artifact_contract.ps1';sha256=$scriptHash}
    runtime = [ordered]@{powershell=$PSVersionTable.PSVersion.ToString();test_json_module=(Get-Command Test-Json).Version.ToString()}
    cases = $rows
    all_cases_pass = @($rows | Where-Object pass -eq $false).Count -eq 0
    corrections = @(
        'The first harness run collapsed an empty patched dissent array to null through PowerShell pipeline enumeration, causing structural rejection before the intended semantic dissent-erasure check.',
        'The first repair wrapped scalar patch values and did not reliably delete a property. Patch application now clones the patch property internally with ConvertFrom-Json -NoEnumerate and verifies deletion.'
    )
    protected_real_bodies_used = $false
    claim = 'Synthetic structural and bounded semantic contract behavior only; not actual privacy enforcement, consent, qualification, cultural benefit, peer consensus or runtime evidence.'
}
$result | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $resultPath -Encoding utf8NoBOM
$result | ConvertTo-Json -Depth 100
if (-not $result.all_cases_pass) { exit 1 }
