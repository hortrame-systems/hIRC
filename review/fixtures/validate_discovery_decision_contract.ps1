$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..\..')).Path
$schemaPath = Join-Path $root 'review\contracts\hirc-discovery-decision.candidate.schema.json'
$fixturePath = Join-Path $root 'review\fixtures\discovery-decision-contract-cases-v1.json'
$resultPath = Join-Path $root 'review\fixtures\discovery-decision-contract-validation-v1.json'
$fixtures = Get-Content -LiteralPath $fixturePath -Raw -Encoding UTF8 | ConvertFrom-Json -Depth 100

function Copy-Object($value) { return (ConvertFrom-Json -InputObject (ConvertTo-Json -InputObject $value -Depth 100 -Compress) -Depth 100) }
function Set-ObjectPath($target, $patch) {
    [string]$path = $patch.path; $parts = $path.Split('.'); $current = $target
    for ($i=0; $i -lt $parts.Count-1; $i++) { $current=$current.($parts[$i]); if($null -eq $current){throw "missing patch parent: $path"} }
    $name=$parts[$parts.Count-1]; $raw=$patch.PSObject.Properties['value'].Value
    $copy=ConvertFrom-Json -InputObject (ConvertTo-Json -InputObject $raw -Depth 100 -Compress) -Depth 100 -NoEnumerate
    $current | Add-Member -NotePropertyName $name -NotePropertyValue $copy -Force
}
function Test-Semantics($p) {
    $errors=[System.Collections.Generic.List[string]]::new(); $candidates=@($p.candidate_set.items); $results=@($p.result.items); $exclusions=@($p.result.exclusions)
    if($p.state -eq 'HELD'){
        if(@($p.holds).Count -eq 0){$errors.Add('held-without-reason')}
        if($results.Count -gt 0){$errors.Add('held-ranking-active')}
    } elseif(@($candidates.source_ref|Sort-Object -Unique).Count -lt 2){$errors.Add('one-authority-feed')}
    $byId=@{}; foreach($c in $candidates){if($byId.ContainsKey($c.artifact_ref)){$errors.Add('duplicate-candidate')}else{$byId[$c.artifact_ref]=$c}}
    $represented=@{}; foreach($r in $results){
        $represented[$r.artifact_ref]=$true
        if(-not $byId.ContainsKey($r.artifact_ref)){$errors.Add('result-not-candidate');continue}
        $c=$byId[$r.artifact_ref]
        if($r.route_ref -notin @($c.route_refs)){$errors.Add('route-not-declared')}
        if($r.original_ref -ne $c.source_ref){$errors.Add('original-ref-mismatch')}
        if(@($r.rationale_refs).Count -eq 0 -or [string]::IsNullOrWhiteSpace($r.uncertainty)){$errors.Add('opaque-result')}
    }
    foreach($e in $exclusions){$represented[$e.artifact_ref]=$true;if(-not $byId.ContainsKey($e.artifact_ref)){$errors.Add('exclusion-not-candidate')}}
    if($p.state -ne 'HELD'){foreach($c in $candidates){if($c.eligible -eq $true -and -not $represented.ContainsKey($c.artifact_ref)){$errors.Add($(if($c.minority_or_dissent){'suppressed-minority-route'}else{'undisclosed-exclusion'}))}}}
    if($p.variation.mode -eq 'BOUNDED_RANDOM' -and ([string]::IsNullOrWhiteSpace($p.variation.seed_commitment_ref) -or [string]::IsNullOrWhiteSpace($p.variation.replay_ref))){$errors.Add('unreplayable-randomness')}
    if($p.variation.independence_claim -ne $false){$errors.Add('randomness-as-independence')}
    if($p.escape.direct_source_retrieval -ne $true -or $p.escape.permitted_originals_reachable -ne $true -or $p.escape.dissent_reachable -ne $true){$errors.Add('source-escape-missing')}
    if($p.authority_effect -ne 'NONE' -or $p.reliability_effect -ne 'NONE'){$errors.Add('authority-or-reliability-effect')}
    return @($errors|Sort-Object -Unique)
}

$rows=@(); foreach($case in $fixtures.cases){
    $payload=Copy-Object $fixtures.base; foreach($patch in @($case.patches)){if($patch.op -ne 'set'){throw "unsupported patch"};Set-ObjectPath $payload $patch}
    $json=$payload|ConvertTo-Json -Depth 100; $structuralErrors=@(); $ok=Test-Json -Json $json -SchemaFile $schemaPath -ErrorAction SilentlyContinue -ErrorVariable structuralErrors
    $semanticErrors=if($ok){@(Test-Semantics $payload)}else{@()}; $ss=if($ok){'ACCEPT'}else{'REJECT'}; $ms=if(-not $ok){'NOT_RUN'}elseif($semanticErrors.Count -eq 0){'ACCEPT'}else{'REJECT'}
    $rows += [ordered]@{name=$case.name;expected_structural=$case.expected_structural;actual_structural=$ss;expected_semantic=$case.expected_semantic;actual_semantic=$ms;structural_error_count=@($structuralErrors).Count;semantic_errors=@($semanticErrors);pass=($ss -eq $case.expected_structural -and $ms -eq $case.expected_semantic)}
}
$result=[ordered]@{
    schema='hirc.discovery-decision-contract-validation/1';stone='M03-S008'
    schema_binding=[ordered]@{path='review/contracts/hirc-discovery-decision.candidate.schema.json';sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $schemaPath).Hash.ToLower()}
    fixture_binding=[ordered]@{path='review/fixtures/discovery-decision-contract-cases-v1.json';sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $fixturePath).Hash.ToLower()}
    harness_binding=[ordered]@{path='review/fixtures/validate_discovery_decision_contract.ps1';sha256=(Get-FileHash -Algorithm SHA256 -LiteralPath $PSCommandPath).Hash.ToLower()}
    runtime=[ordered]@{powershell=$PSVersionTable.PSVersion.ToString();test_json_module=(Get-Command Test-Json).Version.ToString()}
    cases=$rows;all_cases_pass=@($rows|Where-Object pass -eq $false).Count -eq 0;protected_real_bodies_used=$false
    claim='Synthetic structural and bounded semantic discovery behavior only; not recommendation quality, independence, privacy enforcement, consent, peer consensus or runtime evidence.'
}
$resultJson=($result|ConvertTo-Json -Depth 100)-replace "`r`n","`n"
[IO.File]::WriteAllText($resultPath,$resultJson+"`n",[Text.UTF8Encoding]::new($false))
$resultJson
if(-not $result.all_cases_pass){exit 1}
