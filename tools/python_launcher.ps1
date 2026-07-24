function Resolve-AnyangPython {
    param([string]$ExplicitPython)

    $selected = $null
    if ($ExplicitPython) {
        $selected = $ExplicitPython
    } elseif ($env:ANYANG_PYTHON) {
        $selected = $env:ANYANG_PYTHON
    } else {
        # Prefer the repository-local environment when bootstrapped. It persists
        # across agent sessions and is isolated from ephemeral Codex runtimes.
        $repoVenv = Join-Path $PSScriptRoot '..\.venv\Scripts\python.exe'
        if (Test-Path -LiteralPath $repoVenv -PathType Leaf) {
            $selected = $repoVenv
        } elseif ($env:USERPROFILE) {
            # Fall back to the bundled runtime for first-run commands.
            $codexPython = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
            if (Test-Path -LiteralPath $codexPython -PathType Leaf) {
                $selected = $codexPython
            }
        }
        if (-not $selected) {
            $pathPython = Get-Command python -ErrorAction SilentlyContinue
            if ($pathPython -and $pathPython.Source -and (Test-Path -LiteralPath $pathPython.Source -PathType Leaf)) {
                $selected = $pathPython.Source
            }
        }
        if (-not $selected) {
            $python3 = Get-Command python3 -ErrorAction SilentlyContinue
            if ($python3 -and $python3.Source -and (Test-Path -LiteralPath $python3.Source -PathType Leaf)) {
                $selected = $python3.Source
            }
        }
    }

    if (-not $selected -or -not (Test-Path -LiteralPath $selected -PathType Leaf)) {
        throw 'Python 3.10+ was not found. Pass -Python <path> or set ANYANG_PYTHON.'
    }
    return (Resolve-Path -LiteralPath $selected).Path
}
