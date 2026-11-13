# TagLine / tagline-android debug build on Windows (MSYS2 FFmpeg + host Rust).
# Does not adb-install; run install-android-debug.ps1 when ready.
$ErrorActionPreference = "Stop"
$src = (Resolve-Path "$PSScriptRoot\..\src").Path
$sdk = $env:ANDROID_HOME
if (-not $sdk) { $sdk = "$env:LOCALAPPDATA\Android\Sdk" }
$ndk = Get-ChildItem "$sdk\ndk" | Sort-Object Name | Select-Object -Last 1
if (-not $ndk) { throw "No NDK under $sdk\ndk" }
$ndkPath = $ndk.FullName
$ndkBin = "$ndkPath\toolchains\llvm\prebuilt\windows-x86_64\bin"
$ninja = (Get-Command ninja -ErrorAction SilentlyContinue).Source
if (-not $ninja) {
    throw "ninja not in PATH (winget install Ninja-build.Ninja)"
}
$sysroot = "$ndkPath\toolchains\llvm\prebuilt\windows-x86_64\sysroot"
$clangInc = "$ndkPath\toolchains\llvm\prebuilt\windows-x86_64\lib\clang\19\include"
$bindgenExtra = "--target=aarch64-linux-android26 --sysroot=`"$sysroot`" -isystem `"$clangInc`" -isystem `"$sysroot\usr\include`""
$ffmpeg = "$src\vendor\ffmpeg\aarch64-linux-android"
if (-not (Test-Path "$ffmpeg\lib")) {
    throw "Run ffmpeg-mobile.sh in MSYS2 first (see README Phones section)."
}
$llvm = "C:\Program Files\LLVM\bin"
if (-not (Test-Path "$llvm\libclang.dll")) {
    throw "Install LLVM (winget install LLVM.LLVM) for bindgen."
}
$javaHome = $env:JAVA_HOME
if (-not $javaHome -or -not (Test-Path "$javaHome\bin\javac.exe")) {
    $javaHome = "C:\Program Files\Java\jdk-24"
}
if (-not (Test-Path "$javaHome\bin\javac.exe")) {
    throw "Set JAVA_HOME to a JDK (javac) for Slint Android helper."
}
$platform = Get-ChildItem "$sdk\platforms\android-*" | Sort-Object Name | Select-Object -Last 1
$env:JAVA_HOME = $javaHome
$env:PATH = "C:\Program Files\CMake\bin;$ndkBin;$llvm;$javaHome\bin;$env:PATH"
$env:CMAKE_GENERATOR = "Ninja"
$env:CMAKE_MAKE_PROGRAM = $ninja
$env:FFMPEG_DIR = $ffmpeg
$env:TAGLINE_ANDROID_LIBS = "$src\vendor\android\jniLibs\arm64-v8a"
$env:ANDROID_HOME = $sdk
$env:ANDROID_NDK_HOME = $ndkPath
$env:ANDROID_NDK_ROOT = $ndkPath
$env:ANDROID_NDK = $ndkPath
$env:LIBCLANG_PATH = $llvm
$env:BINDGEN_EXTRA_CLANG_ARGS = $bindgenExtra
$env:BINDGEN_EXTRA_CLANG_ARGS_aarch64_linux_android = $bindgenExtra
$env:ANDROID_JAR = "$($platform.FullName)\android.jar"
$env:RUSTFLAGS = "-C link-arg=-Wl,-z,max-page-size=16384"
$linker = "$ndkBin\aarch64-linux-android26-clang.cmd"
$env:CARGO_TARGET_AARCH64_LINUX_ANDROID_LINKER = $linker
$env:CC_aarch64_linux_android = $linker
$env:CXX_aarch64_linux_android = "$ndkBin\aarch64-linux-android26-clang++.cmd"
$env:AR_aarch64_linux_android = "$ndkBin\llvm-ar.exe"
Remove-Item Env:CC, Env:CXX, Env:CLANG_PATH, Env:CMAKE_C_COMPILER, Env:CMAKE_CXX_COMPILER -ErrorAction SilentlyContinue
Push-Location $src
try {
    cargo build -p tagline-android --target aarch64-linux-android
    cargo apk build -p tagline-android
    $apk = @(
        Get-ChildItem -ErrorAction SilentlyContinue target\debug\apk\TagLine.apk
        Get-ChildItem -Recurse -ErrorAction SilentlyContinue target\cargo-apk -Filter *.apk
    ) | Sort-Object LastWriteTime | Select-Object -Last 1
    if ($apk) {
        Copy-Item $apk.FullName (Join-Path (Split-Path $src -Parent) "TagLine-debug.apk") -Force
        Write-Host "APK: $(Join-Path (Split-Path $src -Parent) 'TagLine-debug.apk')"
    }
}
finally {
    Pop-Location
}
