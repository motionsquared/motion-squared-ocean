[CmdletBinding()]
param(
    [string]$SdkRoot = 'C:\code\c4d-sdk-2026',
    [string]$CMake = 'cmake',
    [string]$Python = 'python',
    [string]$Configuration = 'Release',
    [string]$Toolset = 'ClangCL',
    [int]$Jobs = 1,
    [string]$CinemaExecutable = 'C:/Program Files/Maxon Cinema 4D 2026/Cinema 4D.exe'
)
$ErrorActionPreference = 'Stop'
$Python = (& $Python -c 'import sys; print(sys.executable)').Trim()
if ($LASTEXITCODE -ne 0) { throw 'Python 3 is required for the Maxon source processor.' }
$oceanRoot = Split-Path -Parent $PSScriptRoot
$oceanBuild = Join-Path $oceanRoot "build/$Toolset"
New-Item -ItemType Directory -Path $oceanBuild -Force | Out-Null
$oceanCustomPaths = Join-Path $oceanBuild 'custom_paths.txt'
Set-Content -LiteralPath $oceanCustomPaths -Value ('MODULE ' + ($oceanRoot -replace '\\','/'))
& $CMake -S $SdkRoot -B $oceanBuild -G 'Visual Studio 17 2022' -A 'x64,version=10.0.20348.0' -T $Toolset "-DMAXON_SDK_CUSTOM_PATHS_FILE=$oceanCustomPaths" "-DPython3_EXECUTABLE=$Python" "-DMAXON_C4D_EXECUTABLE=$CinemaExecutable"
if ($LASTEXITCODE -ne 0) { throw 'CMake configuration failed.' }
& $CMake --build $oceanBuild --config $Configuration --target motion-squared-ocean --parallel $Jobs -- /p:CL_MPCount=$Jobs /nodeReuse:false
if ($LASTEXITCODE -ne 0) { throw 'Plugin compilation failed.' }
