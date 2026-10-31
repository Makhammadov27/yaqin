param([switch]$Lan)
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$php = 'C:\xampp\php\php.exe'
if (-not (Test-Path -LiteralPath $php)) { throw 'XAMPP PHP topilmadi. PHP manzilini sozlang.' }
$listen = if ($Lan) { '0.0.0.0:4180' } else { '127.0.0.1:4180' }
Write-Host 'Yaqin: http://localhost:4180'
& $php -d upload_max_filesize=20M -d post_max_size=25M -S $listen -t public
