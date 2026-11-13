# Build TagLine debug APK from this fork on Windows (needs FFmpeg in vendor/).
$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot\..").Path
$src = "$root\src"
$sdk = if ($env:ANDROID_HOME) { $env:ANDROID_HOME } else { "$env:LOCALAPPDATA\Android\Sdk" }
$ndk = Get-ChildItem "$sdk\ndk" | Sort-Object Name | Select-Object -Last 1
if (-not $ndk) { throw "Install Android NDK via SDK Manager" }

$env:ANDROID_HOME = $sdk
$env:ANDROID_NDK_HOME = $ndk.FullName
$bash = "C:\Program Files\Git\bin\bash.exe"
if (-not (Test-Path $bash)) { throw "Install Git for Windows (bash)" }

$ffmpegLib = "$src\vendor\ffmpeg\aarch64-linux-android\lib"
if (-not (Test-Path "$ffmpegLib\libavcodec.a")) {
    Write-Host "FFmpeg for Android missing. Use scripts/build-android-docker.ps1 after starting Docker Desktop."
    throw "No FFmpeg at $ffmpegLib"
}

function To-GitBashPath([string]$path) {
    $resolved = (Resolve-Path $path).Path
    if ($resolved -match '^([A-Za-z]):\\(.*)$') {
        $drive = $Matches[1].ToLower()
        $rest = $Matches[2] -replace '\\', '/'
        return "/$drive/$rest"
    }
    throw "Cannot map path for Git Bash: $resolved"
}
$srcBash = To-GitBashPath $src

$cmd = @(
    'export PATH="/c/MinGW/bin:$PATH"'
    "cd $srcBash"
    'scripts/android-libs.sh aarch64-linux-android'
    'eval "$(scripts/mobile-env.sh aarch64-linux-android)"'
    'cargo ndk -t arm64-v8a --platform 26 build -p tagline-android'
    'cargo apk build -p tagline-android'
) -join ' && '
& $bash -lc $cmd
if ($LASTEXITCODE -ne 0) { throw "Android build failed (exit $LASTEXITCODE)" }

$apk = Get-ChildItem -Path "$src\target\cargo-apk" -Recurse -Filter "*.apk" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $apk) { throw "APK not found under src/target/cargo-apk" }
Copy-Item $apk.FullName "$root\TagLine-debug.apk" -Force
Write-Host "Built: $root\TagLine-debug.apk"
