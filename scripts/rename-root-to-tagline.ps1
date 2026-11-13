# Rename repo folder Concat -> TagLine (close Cursor/terminals first).
$ErrorActionPreference = "Stop"
$parent = "C:\Users\anilk\Projects"
$old = Join-Path $parent "Concat"
$new = Join-Path $parent "TagLine"
if (-not (Test-Path $old)) {
    if (Test-Path $new) {
        Write-Host "Already at $new"
        exit 0
    }
    throw "Neither $old nor $new exists."
}
if (Test-Path $new) {
    throw "$new already exists; remove or merge first."
}
Rename-Item -LiteralPath $old -NewName "TagLine"
Write-Host "Renamed $old -> $new"
Write-Host "Reopen Cursor: $new\src"
