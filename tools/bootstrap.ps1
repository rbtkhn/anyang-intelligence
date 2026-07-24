[CmdletBinding()]
param([switch]$Refresh)

$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$venv = Join-Path $root '.venv'
. (Join-Path $PSScriptRoot 'python_launcher.ps1')
$base = Resolve-AnyangPython
$venvPython = Join-Path $venv 'Scripts\python.exe'

if ($Refresh -and (Test-Path -LiteralPath $venv)) {
    Remove-Item -LiteralPath $venv -Recurse -Force
}
if (-not (Test-Path -LiteralPath $venvPython -PathType Leaf)) {
    & $base -m venv $venv
}
& $venvPython -m pip install --disable-pip-version-check PyYAML pytest
Write-Host "Persistent repository environment ready: $venvPython"
