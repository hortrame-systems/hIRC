$ErrorActionPreference='Stop'
$root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$schemaPath=Join-Path $root 'review\contracts\hirc-release-profile.candidate.schema.json'
$fixturePath=Join-Path $root 'review\fixtures\security-release-profile-cases-v1.json'
$outputPath=Join-Path $root 'review\fixtures\security-release-profile-validation-v1.json'
$fixture=Get-Content -Raw $fixturePath|ConvertFrom-Json
function Copy-Record($record){return($record|ConvertTo-Json -Depth 50|ConvertFrom-Json)}
function Test-Structural($record){return(Test-Json -Json ($record|ConvertTo-Json -Depth 50) -SchemaFile $schemaPath -ErrorAction SilentlyContinue)}
function Get-TextSha($text){$a=[Security.Cryptography.SHA256]::Create();try{return [Convert]::ToHexString($a.ComputeHash([Text.Encoding]::UTF8.GetBytes($text))).ToLower()}finally{$a.Dispose()}}
function Test-Semantic($record){
  $reasons=@()
  $controls=@($record.core_controls.control_id);$tests=@($record.tests.test_id)
  if(@($controls|Sort-Object -Unique).Count-ne$controls.Count){$reasons+='duplicate control id'}
  if(@($tests|Sort-Object -Unique).Count-ne$tests.Count){$reasons+='duplicate test id'}
  if((Compare-Object @($record.required_control_ids|Sort-Object) @($controls|Sort-Object)).Count-ne0){$reasons+='required control coverage mismatch'}
  if((Compare-Object @($record.required_test_ids|Sort-Object) @($tests|Sort-Object)).Count-ne0){$reasons+='required test coverage mismatch'}
  if(@($record.tests|Where-Object { $_.applicability -eq 'REQUIRED' }).Count -lt 1){$reasons+='no REQUIRED test'}
  $enabled=@($record.enabled_capabilities|ForEach-Object{$_.capability_id});$disabled=@($record.disabled_capabilities|ForEach-Object{$_.capability_id})
  if(@($enabled|Sort-Object -Unique).Count-ne$enabled.Count -or @($disabled|Sort-Object -Unique).Count-ne$disabled.Count){$reasons+='duplicate capability id'}
  if((Compare-Object $enabled $disabled -IncludeEqual -ExcludeDifferent).Count-gt0){$reasons+='capability both enabled and disabled'}
  foreach($capability in $record.enabled_capabilities){foreach($id in $capability.control_refs){$item=@($record.core_controls|Where-Object { $_.control_id -eq $id });if($item.Count -ne 1 -or $item[0].state -ne 'PASS'){$reasons+="enabled control not resolved PASS $id"}};foreach($id in $capability.test_refs){$item=@($record.tests|Where-Object { $_.test_id -eq $id });if($item.Count -ne 1 -or $item[0].applicability -ne 'REQUIRED' -or $item[0].state -ne 'PASS'){$reasons+="enabled test not REQUIRED PASS $id"}}}
  $controlSet=Get-TextSha ((@($record.required_control_ids|Sort-Object))-join"`n")
  $testSet=Get-TextSha ((@($record.required_test_ids|Sort-Object))-join"`n")
  if($record.assurance_binding.required_control_set_sha256 -ne $controlSet){$reasons+='assurance control-set hash mismatch'}
  if($record.assurance_binding.required_test_set_sha256 -ne $testSet){$reasons+='assurance test-set hash mismatch'}
  $evaluated=[datetime]::MinValue;if(-not [datetime]::TryParse($record.evaluated_at,[ref]$evaluated)){$reasons+='invalid evaluated_at'}
  $resolved=[datetime]::MinValue;if(-not [datetime]::TryParse($record.assurance_binding.resolved_at,[ref]$resolved) -or $resolved -gt $evaluated){$reasons+='invalid assurance resolved_at'}
  foreach($disabled in $record.disabled_capabilities){$observed=[datetime]::MinValue;if(-not [datetime]::TryParse($disabled.absence_proof.observed_at,[ref]$observed) -or $observed -gt $evaluated){$reasons+='invalid absence proof time'};if($disabled.absence_proof.subject_sha256 -ne $record.release_subject_sha256){$reasons+='absence proof subject mismatch'}}
  if($record.observed_release){$observed=[datetime]::MinValue;if(-not [datetime]::TryParse($record.observed_release.observed_at,[ref]$observed) -or $observed -gt $evaluated){$reasons+='invalid observed release time'};if($record.observed_release.subject_sha256 -ne $record.release_subject_sha256){$reasons+='observed subject mismatch'};if($record.observed_release.build_sha256 -ne $record.build_sha256){$reasons+='observed build mismatch'};if($record.observed_release.environment_manifest_sha256 -ne $record.environment_manifest_sha256){$reasons+='observed environment mismatch'}}
  return [pscustomobject]@{valid=($reasons.Count -eq 0);reasons=$reasons}
}
function Test-Combined($record){$s=Test-Structural $record;$m=Test-Semantic $record;return [pscustomobject]@{structural=$s;semantic=$m.valid;reasons=$m.reasons;accepted=($s -and $m.valid)}}
$ready=Copy-Record $fixture.ready
$released=Copy-Record $fixture.ready;$released.state='RELEASED';$released|Add-Member -NotePropertyName observed_release -NotePropertyValue $fixture.released_observation
$enabledOnly=Copy-Record $ready;$enabledOnly.disabled_capabilities=@()
$disabledOnly=Copy-Record $ready;$disabledOnly.enabled_capabilities=@()
$positive=@(
  [pscustomobject]@{name='ready';result=(Test-Combined $ready)},
  [pscustomobject]@{name='released';result=(Test-Combined $released)},
  [pscustomobject]@{name='enabled_only';result=(Test-Combined $enabledOnly)},
  [pscustomobject]@{name='disabled_only';result=(Test-Combined $disabledOnly)}
)
$cases=@();function Add-Adverse($name,$record){$r=Test-Combined $record;$script:cases+=[pscustomobject]@{name=$name;structural=$r.structural;semantic=$r.semantic;reasons=$r.reasons;rejected=(-not$r.accepted)}}
$r=Copy-Record $ready;$r.core_controls=@();Add-Adverse 'empty_controls' $r
$r=Copy-Record $ready;$r.tests=@();Add-Adverse 'empty_tests' $r
$r=Copy-Record $ready;$r.tests[0].applicability='NOT_APPLICABLE';$r.tests[0].state='NOT_APPLICABLE';Add-Adverse 'no_required_test' $r
$r=Copy-Record $ready;$r.disabled_capabilities[0].listener_absence_verified=$false;Add-Adverse 'disabled_listener_unverified' $r
$r=Copy-Record $ready;$r.disabled_capabilities[0].capability_id='capability:local-analysis';Add-Adverse 'enabled_and_disabled' $r
$r=Copy-Record $released;$r.PSObject.Properties.Remove('observed_release');Add-Adverse 'released_unobserved' $r
$r=Copy-Record $ready;$r.release_evidence_refs=@();Add-Adverse 'release_without_evidence' $r
$r=Copy-Record $ready;$r.required_control_ids=@('control:other');Add-Adverse 'control_coverage_mismatch' $r
$r=Copy-Record $ready;$r.enabled_capabilities[0].control_refs=@();Add-Adverse 'enabled_without_control_refs' $r
$r=Copy-Record $ready;$r.core_controls[0].evidence_refs=@();Add-Adverse 'pass_control_without_evidence' $r
$r=Copy-Record $ready;$r.disabled_capabilities[0].enforcement_refs=@();Add-Adverse 'disabled_without_enforcement_refs' $r
$r=Copy-Record $ready;$r.disabled_capabilities[0].absence_proof.evidence_refs=@();Add-Adverse 'absence_proof_without_evidence' $r
$r=Copy-Record $ready;$r.evaluated_at='not-a-date';Add-Adverse 'invalid_evaluated_timestamp' $r
$r=Copy-Record $ready;$r.assurance_binding.required_control_set_sha256='9999999999999999999999999999999999999999999999999999999999999999';Add-Adverse 'assurance_set_hash_mismatch' $r
$r=Copy-Record $released;$r.observed_release.observed_at='2999-01-01T00:00:00Z';Add-Adverse 'future_observed_release' $r
$r=Copy-Record $released;$r.observed_release.subject_sha256='9999999999999999999999999999999999999999999999999999999999999999';Add-Adverse 'observed_subject_mismatch' $r
$r=Copy-Record $ready;$r.tests[0].applicability='NOT_APPLICABLE';$r.tests[0].state='NOT_APPLICABLE';$r.tests += [pscustomobject]@{test_id='test:other';applicability='REQUIRED';state='PASS';evidence_refs=@('evidence:other')};$r.required_test_ids=@('test:core','test:other');$r.assurance_binding.required_test_set_sha256=(Get-TextSha ((@($r.required_test_ids|Sort-Object))-join"`n"));Add-Adverse 'capability_references_not_applicable_test' $r
$state=if(($positive|Where-Object{-not$_.result.accepted}).Count-eq0-and($cases|Where-Object{-not$_.rejected}).Count-eq0){'PASS'}else{'FAIL'}
$result=[pscustomobject]@{schema='hirc.security-release-profile-validation/1';state=$state;target=[pscustomobject]@{path='review/contracts/hirc-release-profile.candidate.schema.json';sha256=(Get-FileHash $schemaPath -Algorithm SHA256).Hash.ToLower()};fixture=[pscustomobject]@{path='review/fixtures/security-release-profile-cases-v1.json';sha256=(Get-FileHash $fixturePath -Algorithm SHA256).Hash.ToLower()};positive=$positive;adverse=$cases;nonclaim='Schema plus deterministic coverage/disjointness validation only; not deployment, security assurance, independent review or release authorization.'}
$rendered=$result|ConvertTo-Json -Depth 12;[IO.File]::WriteAllText($outputPath,$rendered+"`n",[Text.UTF8Encoding]::new($false));$rendered;if($state-ne'PASS'){exit 1}
