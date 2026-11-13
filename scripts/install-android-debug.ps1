# Install fork debug APK and launch TagLine on the connected phone.
# Package is app.tagline.editor (not app.concat.editor); uninstall the old app first if both are installed.
param([string]$Apk = (Resolve-Path "$PSScriptRoot\..\TagLine-debug.apk").Path)

if (-not (Test-Path $Apk)) {
    throw "Missing $Apk — run .\scripts\build-android-debug.ps1 or build-android-docker.ps1 first"
}

adb wait-for-device
adb install -r $Apk
adb shell am start -n app.tagline.editor/android.app.NativeActivity
Write-Host "Logcat: adb logcat | findstr /i concat TagLine"
