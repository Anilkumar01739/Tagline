#!/usr/bin/env bash
# One-shot TagLine/Concat Android debug APK on Linux (Docker on Windows).
set -euo pipefail

cd /work/src
export ANDROID_HOME="${ANDROID_HOME:-/sdk}"
export ANDROID_NDK_HOME="${ANDROID_NDK_HOME:-$(ls -d "$ANDROID_HOME"/ndk/* 2>/dev/null | sort -V | tail -1)}"

scripts/android-libs.sh aarch64-linux-android
rm -rf vendor/ffmpeg/src/build-aarch64-linux-android vendor/ffmpeg/aarch64-linux-android
scripts/ffmpeg-mobile.sh aarch64-linux-android
# shellcheck disable=SC1091
eval "$(scripts/mobile-env.sh aarch64-linux-android)"

cargo ndk -t arm64-v8a --platform 26 build -p tagline-android
cargo apk build -p tagline-android

apk=$(find target/cargo-apk -name '*.apk' 2>/dev/null | head -1)
echo "APK: $apk"
cp "$apk" /work/TagLine-debug.apk
