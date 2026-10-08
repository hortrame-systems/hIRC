$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$fixturePath = Join-Path $root 'review\fixtures\waymark-trust-contract-cases-v1.json'
$fixture = Get-Content -Raw $fixturePath | ConvertFrom-Json

$schemaByBase = @{
    request = Join-Path $root 'review\contracts\hirc-request-case.candidate.schema.v2.json'
    reliance = Join-Path $root 'review\contracts\hirc-bayesian-reliance.candidate.schema.v2.json'
    competition = Join-Path $root 'review\contracts\hirc-cooperative-competition-charter.candidate.schema.v2.json'
}

$bindingResults = foreach ($binding in $fixture.schema_bindings) {
    $path = (Resolve-Path (Join-Path (Split-Path $fixturePath) $binding.path)).Path
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower()
    [pscustomobject]@{
        path = $binding.path
        expected_sha256 = $binding.sha256
        actual_sha256 = $actual
        pass = ($actual -eq $binding.sha256)
    }
}

$targetBindings = foreach ($base in @('request','reliance','competition')) {
    $path = (Resolve-Path $schemaByBase[$base]).Path
    [pscustomobject]@{
        base = $base
        path = $path.Substring($root.Length + 1).Replace('\','/')
        sha256 = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLower()
    }
}

function Get-StringSha256 {
    param([Parameter(Mandatory)] [string] $Text)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
    $algorithm = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [System.Convert]::ToHexString($algorithm.ComputeHash($bytes)).ToLower()
    } finally {
        $algorithm.Dispose()
    }
}

function Set-FixturePathValue {
    param(
        [Parameter(Mandatory)] $Object,
        [Parameter(Mandatory)] [object[]] $Path,
        [Parameter(Mandatory)] $Value
    )
    $cursor = $Object
    for ($i = 0; $i -lt $Path.Count - 1; $i++) {
        $step = $Path[$i]
        if ($step -is [int] -or $step -is [long]) {
            $cursor = $cursor[[int]$step]
        } else {
            $cursor = $cursor.$step
        }
    }
    $last = $Path[-1]
    if ($last -is [int] -or $last -is [long]) {
        $cursor[[int]$last] = $Value
    } else {
        $cursor.$last = $Value
    }
}

function Test-RequestSemantic {
    param($Record)
    $reasons = @()
    if ($Record.action_disposition.state -eq 'PROCEED_AFTER_PUSHBACK') {
        if ($Record.participation.state -ne 'WILLING') { $reasons += 'participation is not WILLING' }
        if (-not $Record.authority.current) { $reasons += 'authority is not current' }
        if ($Record.action_disposition.effect_gate_state -ne 'PASS') { $reasons += 'effect gate is not PASS' }
        foreach ($name in @('clear_intent','permitted','local','reversible','low_cost','no_meaningful_third_party','no_sensitive_data','no_security_legal_financial_or_irreversible_effect','objection_understood','agent_willing')) {
            if (-not $Record.low_consequence.$name) { $reasons += "low_consequence.$name is not true" }
        }
    }
    [pscustomobject]@{ valid = ($reasons.Count -eq 0); reasons = $reasons }
}

function ConvertTo-V2Contract {
    param(
        [Parameter(Mandatory)] [string] $Base,
        [Parameter(Mandatory)] $Record
    )
    switch ($Base) {
        request {
            $Record.schema_version = 'hirc.request-case/2-candidate'
            $Record.source | Add-Member -NotePropertyName admission_state -NotePropertyValue 'ADMITTED_BEFORE_CASE_CREATION'
            $Record.source | Add-Member -NotePropertyName admission_ref -NotePropertyValue 'synthetic:privacy-admission'
            foreach ($interpretation in $Record.interpretations) {
                $value = [double]$interpretation.confidence
                $interpretation.confidence = [pscustomobject]@{
                    state = 'ESTIMATED'
                    value = $value
                    method_ref = 'synthetic:declared-estimate'
                    uncertainty_ref = 'synthetic:estimate-limits'
                }
            }
            if ($null -ne $Record.low_consequence) {
                $Record.low_consequence | Add-Member -NotePropertyName profile_ref -NotePropertyValue 'profile:isolated-personal-theme'
                $Record.low_consequence | Add-Member -NotePropertyName profile_version -NotePropertyValue '1'
                $Record.low_consequence | Add-Member -NotePropertyName current_permission_rechecked -NotePropertyValue $true
                $Record.low_consequence | Add-Member -NotePropertyName changed_material_premises -NotePropertyValue $false
            }
        }
        reliance {
            $Record.schema_version = 'hirc.bayesian-reliance/2-candidate'
            $Record.metric | Add-Member -NotePropertyName definition_signature_verification_ref -NotePropertyValue 'synthetic:metric-signature-check'
            $Record.governance | Add-Member -NotePropertyName prohibited_inference_refs -NotePropertyValue @('prohibition:global-worth-score','prohibition:cross-domain-transfer')
            $Record.governance | Add-Member -NotePropertyName global_rank_or_sort_prohibited -NotePropertyValue $true
            $Record.governance | Add-Member -NotePropertyName refusal_nochange_abstention_not_negative_evidence -NotePropertyValue $true
            $Record.governance | Add-Member -NotePropertyName opportunity_feedback_loop_review_ref -NotePropertyValue 'synthetic:opportunity-feedback-review'
            if ($Record.state -eq 'ACTIVE_FOR_DECLARED_SCOPE') {
                $Record | Add-Member -NotePropertyName model_fit -NotePropertyValue ([pscustomobject]@{
                    prior_sensitivity_ref = 'synthetic:prior-sensitivity'
                    posterior_predictive_check_ref = 'synthetic:posterior-predictive-check'
                    dependence_report_ref = 'synthetic:dependence-report'
                    missingness_selection_report_ref = 'synthetic:missingness-selection-report'
                    calibration_ref = 'synthetic:calibration-report'
                    drift_report_ref = 'synthetic:drift-report'
                    model_limit_refs = @('synthetic:no-performance-validation')
                })
            }
        }
        competition {
            $Record.schema_version = 'hirc.cooperative-competition-charter/2-candidate'
            $Record.objective | Add-Member -NotePropertyName protected_quality_refs -NotePropertyValue @('quality:correctness','quality:privacy','quality:refusal','quality:traceability')
            $Record.objective | Add-Member -NotePropertyName non_compensation_rule_ref -NotePropertyValue 'rule:no-quality-offset'
            $Record.credit_and_memory | Add-Member -NotePropertyName no_global_participant_rank -NotePropertyValue $true
            $Record.credit_and_memory | Add-Member -NotePropertyName credit_is_task_scoped -NotePropertyValue $true
            if ($Record.state -eq 'ACTIVE') {
                $distinct = @($Record.participants.participant_id | Sort-Object -Unique)
                $allAccepted = @($Record.participants | Where-Object { $_.consent_state -eq 'ACCEPTED' }).Count -eq $Record.participants.Count
                $Record | Add-Member -NotePropertyName activation_validation -NotePropertyValue ([pscustomobject]@{
                    distinct_participants_verified = ($distinct.Count -eq $Record.participants.Count)
                    current_consent_verified = $allAccepted
                    eligibility_verified = $true
                    reference_closure_ref = 'synthetic:reference-closure'
                    validated_at = '2026-10-08T00:01:00Z'
                })
            }
        }
    }
    return $Record
}

function Test-RelianceSemantic {
    param($Record)
    $reasons = @()
    foreach ($name in @('prior','posterior')) {
        $distribution = $Record.$name
        if ($distribution.family -eq 'BETA') {
            if ($null -eq $distribution.parameters.alpha -or [double]$distribution.parameters.alpha -le 0) { $reasons += "$name Beta alpha must be > 0" }
            if ($null -eq $distribution.parameters.beta -or [double]$distribution.parameters.beta -le 0) { $reasons += "$name Beta beta must be > 0" }
        }
    }
    if ($Record.state -eq 'ACTIVE_FOR_DECLARED_SCOPE' -and -not $Record.metric.signed_definition) {
        $reasons += 'active posterior metric definition is not signed/verified at serialized flag level'
    }
    [pscustomobject]@{ valid = ($reasons.Count -eq 0); reasons = $reasons }
}

function Test-CompetitionSemantic {
    param($Record)
    $reasons = @()
    if ($Record.state -eq 'ACTIVE') {
        if ($Record.participants.Count -lt 2) { $reasons += 'active contest has fewer than two participants' }
        $accepted = @($Record.participants | Where-Object { $_.consent_state -eq 'ACCEPTED' })
        if ($accepted.Count -ne $Record.participants.Count) { $reasons += 'active contest includes non-ACCEPTED participant' }
        $distinct = @($Record.participants.participant_id | Sort-Object -Unique)
        if ($distinct.Count -ne $Record.participants.Count) { $reasons += 'active contest participant identities are not distinct' }
    }
    [pscustomobject]@{ valid = ($reasons.Count -eq 0); reasons = $reasons }
}

$results = foreach ($case in $fixture.cases) {
    $record = $fixture.bases.($case.base) | ConvertTo-Json -Depth 50 | ConvertFrom-Json
    foreach ($patch in $case.patches) {
        Set-FixturePathValue -Object $record -Path @($patch.path) -Value $patch.value
    }
    $record = ConvertTo-V2Contract -Base $case.base -Record $record
    $json = $record | ConvertTo-Json -Depth 50
    $structural = Test-Json -Json $json -SchemaFile $schemaByBase[$case.base] -ErrorAction SilentlyContinue
    $semantic = switch ($case.base) {
        request { Test-RequestSemantic $record }
        reliance { Test-RelianceSemantic $record }
        competition { Test-CompetitionSemantic $record }
    }
    $expected = $case.id.StartsWith('WST-C')
    [pscustomobject]@{
        id = $case.id
        base = $case.base
        expected_semantic_valid = $expected
        structural_v2_valid = $structural
        adapted_input_sha256 = Get-StringSha256 $json
        semantic_valid = $semantic.valid
        semantic_expectation_pass = ($semantic.valid -eq $expected)
        semantic_reasons = $semantic.reasons
        expected_semantic = $case.expected_semantic
    }
}

$state = if (
    ($bindingResults | Where-Object { -not $_.pass }).Count -eq 0 -and
    ($results | Where-Object { $_.structural_v2_valid -ne $_.expected_semantic_valid }).Count -eq 0 -and
    ($results | Where-Object { -not $_.semantic_expectation_pass }).Count -eq 0
) { 'PASS' } else { 'FAIL' }

$testJsonCommand = Get-Command Test-Json
$harnessPath = (Resolve-Path $PSCommandPath).Path

[pscustomobject]@{
    schema = 'hirc.waymark-contract-validation/2.1'
    fixture_path = 'review/fixtures/waymark-trust-contract-cases-v1.json'
    fixture_sha256 = (Get-FileHash -LiteralPath $fixturePath -Algorithm SHA256).Hash.ToLower()
    fixture_source_bindings = $bindingResults
    validation_targets = $targetBindings
    adapter_harness = [pscustomobject]@{
        path = $harnessPath.Substring($root.Length + 1).Replace('\','/')
        sha256 = (Get-FileHash -LiteralPath $harnessPath -Algorithm SHA256).Hash.ToLower()
        adaptation = 'WAYMARK v1 base+patch expansion, then explicit required-field v2 adapter in this exact harness; per-case adapted UTF-8 ConvertTo-Json depth50 hash recorded'
    }
    runtime = [pscustomobject]@{
        powershell_edition = $PSVersionTable.PSEdition
        powershell_version = $PSVersionTable.PSVersion.ToString()
        platform = $PSVersionTable.Platform
        os = $PSVersionTable.OS
        validator_command = $testJsonCommand.Name
        validator_module = $testJsonCommand.ModuleName
        validator_module_version = $testJsonCommand.Version.ToString()
        validator_source = $testJsonCommand.Source
    }
    validator = 'Test-Json against exact v2 candidate targets plus explicit semantic checks in the hash-bound adapter harness'
    state = $state
    cases = $results
    structural_v2_adverse_cases_accepted = @($results | Where-Object { -not $_.expected_semantic_valid -and $_.structural_v2_valid }).Count
    limits = 'Synthetic WAYMARK cases adapted only for explicit v2 fields. Serialized validation flags remain evidence references, not proof; runtime reference closure, privacy admission, dispatch/activation enforcement, statistical validation and security assurance remain separate.'
} | ConvertTo-Json -Depth 12

if ($state -ne 'PASS') { exit 1 }
