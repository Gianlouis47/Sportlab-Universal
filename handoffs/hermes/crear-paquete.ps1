[CmdletBinding()]
param(
    [string]$Destination = (Join-Path ([Environment]::GetFolderPath('Desktop')) 'SportLab-Hermes-20261021')
)
$ErrorActionPreference = 'Stop'
$bundlePath = [IO.Path]::GetFullPath($Destination)
$archivePath = "$bundlePath.zip"
$repoPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..'))
if (-not (Test-Path -LiteralPath (Join-Path $repoPath 'AGENTS.md'))) {
    throw 'Ejecuta este archivo desde handoffs/hermes dentro del checkout Sportlab-Universal.'
}
if (Test-Path -LiteralPath $bundlePath) { throw "La carpeta ya existe: $bundlePath" }
if (Test-Path -LiteralPath $archivePath) { throw "El ZIP ya existe: $archivePath" }
if ($bundlePath.Equals($repoPath, [StringComparison]::OrdinalIgnoreCase) -or
    $bundlePath.StartsWith($repoPath + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Elige un destino fuera del repositorio.'
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw 'Git es necesario para empaquetar únicamente archivos versionados.'
}
$includedPaths = @('AGENTS.md','knowledge','config','sportlab','pyproject.toml','handoffs/hermes')
& git -C $repoPath archive --format=zip "--output=$archivePath" HEAD -- @includedPaths
if ($LASTEXITCODE -ne 0) { throw 'No se pudo generar el ZIP desde el commit local.' }
Expand-Archive -LiteralPath $archivePath -DestinationPath $bundlePath
Write-Output "Carpeta: $bundlePath"
Write-Output "ZIP: $archivePath"
