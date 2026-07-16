[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet('project', 'loop', 'ops', 'coffee', 'dream')]
    [string]$Surface,
    [string]$Python,
    [switch]$Refresh,
    [string]$CacheDir,
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$SurfaceArgs
)

$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot 'python_launcher.ps1')
$selected = Resolve-AnyangPython -ExplicitPython $Python
$runner = Join-Path $PSScriptRoot 'run_repo.py'

$runnerArgs = @()
if ($Refresh) {
    $runnerArgs += '--refresh'
}
if ($CacheDir) {
    $runnerArgs += @('--cache-dir', $CacheDir)
}
$runnerArgs += $Surface
$runnerArgs += $SurfaceArgs

& $selected $runner @runnerArgs
exit $LASTEXITCODE
