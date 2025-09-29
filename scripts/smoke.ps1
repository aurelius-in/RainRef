$ErrorActionPreference = "Stop"

param(
  [string]$Api = "http://localhost:8088",
  [string]$User = "admin@rainref.local",
  [string]$Pass = "admin"
)

Write-Host "RainRef smoke against $Api"

# Login
$login = Invoke-RestMethod -Method Post -Uri "$Api/auth/login" -ContentType 'application/json' -Body (@{username=$User; password=$Pass} | ConvertTo-Json)
$token = $login.access_token
if (-not $token) { throw "login failed" }
Write-Host "Token received"

$headers = @{ Authorization = "Bearer $token" }

# Ingest event
$evt = Invoke-RestMethod -Method Post -Uri "$Api/ref/events" -ContentType 'application/json' -Body (@{source='email'; channel='support'; text='I need activation'; user_ref='u-1'} | ConvertTo-Json) -Headers $headers
Write-Host "Event: $($evt.id)"

# Propose answer
$ans = Invoke-RestMethod -Method Post -Uri "$Api/support/answer" -ContentType 'application/json' -Body (@{source='inbox'; channel='support'; text='I need activation'; user_ref='u-1'} | ConvertTo-Json) -Headers $headers
Write-Host "Ticket: $($ans.ticket_id) Actions: $($ans.actions_suggested.Length)"

# Execute first action
if ($ans.actions_suggested.Length -gt 0) {
  $act = $ans.actions_suggested[0] | ConvertTo-Json -Depth 5
  $exec = Invoke-RestMethod -Method Post -Uri "$Api/action/execute" -ContentType 'application/json' -Body $act -Headers $headers
  Write-Host "Receipt: $($exec.beacon_receipt_id)"
  $rec = Invoke-RestMethod -Method Get -Uri "$Api/audit/$($exec.beacon_receipt_id)" -Headers $headers
  Write-Host "Verified: $($rec.verified)"
}

Write-Host "Smoke OK"


