[CmdletBinding()]
param(
    [string]$Python,
    [switch]$BootstrapOnly,
    [switch]$Refresh,
    [string]$CacheDir
)

$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot 'validate_repo.py'
. (Join-Path $PSScriptRoot 'python_launcher.ps1')
$selected = Resolve-AnyangPython -ExplicitPython $Python

$validatorArgs = @()
if ($BootstrapOnly) {
    $validatorArgs += '--bootstrap-only'
}
if ($Refresh) {
    $validatorArgs += '--refresh'
}
if ($CacheDir) {
    $validatorArgs += @('--cache-dir', $CacheDir)
}

& $selected $validator @validatorArgs
exit $LASTEXITCODE
