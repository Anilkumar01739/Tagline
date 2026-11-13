# Build TagLine debug APK via Docker (recommended on Windows).
$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot\..").Path
$sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { "$env:LOCALAPPDATA\Android\Sdk" }
$ndk = Get-ChildItem "$sdk\ndk" | Sort-Object Name | Select-Object -Last 1
if (-not $ndk) { throw "No NDK under $sdk\ndk" }

docker ps 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    throw "Docker is not running. Start Docker Desktop, wait until 'docker ps' works, then rerun."
}

docker run --rm `
    -v "${root}:/work" `
    -v "${sdk}:/sdk" `
    -e ANDROID_HOME=/sdk `
    -e "ANDROID_NDK_HOME=/sdk/ndk/$($ndk.Name)" `
    ubuntu:24.04 bash -lc @'
set -e
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq build-essential curl pkg-config git openjdk-17-jdk-headless perl python3 ca-certificates
curl -fsSL https://sh.rustup.rs | sh -s -- -y -q
. ~/.cargo/env
rustup target add aarch64-linux-android
cargo install cargo-ndk cargo-apk --locked -q
bash /work/scripts/docker-android-build.sh
'@

Write-Host "APK: $root\TagLine-debug.apk"
Write-Host "Install: .\scripts\install-android-debug.ps1"
