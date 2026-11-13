---
name: run-tagline-android
description: Build, install, and smoke-test the TagLine Android app (Rust + Slint, package app.tagline.editor) after a code change. Use when the user wants to run TagLine on a phone or emulator, test a UI change on device, verify a fix beyond unit tests, or install a CI-built APK. Cargo workspace root is src/, not the repo root.
---

# Running and verifying TagLine (Android)

TagLine on Android is a Rust cdylib (`tagline-android`) inside a Slint activity. The git repo root and the Cargo workspace root are **different** — run `cargo` from `<repo>/src`, not the repo root.

## Repo layout

- Git repo root: e.g. `C:\Users\anilk\Projects\Concat` (Tagline fork).
- Cargo workspace: `<repo>/src` (`Cargo.toml` for the workspace).
- Android shell crate: `src/crates/tagline-android` (`app.tagline.editor`).

## CI APK (no local build)

[Android APK workflow](https://github.com/Anilkumar01739/Tagline/actions/workflows/android-apk.yml) on Linux builds **arm64** release APKs.

1. Open the latest green run → **Artifacts** → **`TagLine-android-arm64`**.
2. Install: `adb install -r TagLine-*-android-arm64.apk`.

## Local build (Windows)

From repo root (needs FFmpeg for Android, NDK, JDK — see `scripts/build-android-windows.ps1`):

```powershell
.\scripts\build-android-windows.ps1
```

APK often lands as `TagLine-debug.apk` at repo root. Install when ready (e.g. `adb install -r …`).

## Linux / macOS (manual)

```bash
src/scripts/ffmpeg-mobile.sh aarch64-linux-android
src/scripts/android-libs.sh aarch64-linux-android
cd "<repo>/src"
eval "$(scripts/mobile-env.sh aarch64-linux-android)"
cargo apk build --release -p tagline-android --target aarch64-linux-android
```

APK under `src/target/.../apk/TagLine.apk`.

## Cheap checks before a full APK build

```bash
cd "<repo>/src"

# Slint + Android shell type-check
cargo check -p tagline-android --target aarch64-linux-android

# Editor UI crate (most .slint edits)
cargo check -p tagline

# CI-style lint for the shell (no desktop workspace)
cargo clippy -p tagline-android --all-targets --no-deps -- -D warnings
```

`.slint` wiring errors often only show up on `cargo check -p tagline` or the Android target check, not on a narrow crate test.

## On-device verification

There is no headless GUI driver for TagLine on Android in a typical session.

1. **Build or download an APK** — confirm the terminal shows success (no `error:` after `cargo apk build`).
2. **Install and open** on phone or emulator — user confirms the screen that exercises the change.
3. **Crashes** — `adb logcat` filtered on `TagLine` / `app.tagline.editor` / Rust panics.

Tell the user exactly what to tap (timeline, export, settings, etc.), not a vague “see if it works.”

## Effects packages

New effect folders under `src/crates/tagline-effects/packages/tagline.<name>/` are picked up at compile time (`build.rs`). If a new package does not appear after rebuild, try `cargo clean -p tagline-effects` before debugging the package itself.

## Quick checklist

1. Run `cargo check -p tagline-android --target aarch64-linux-android` (and `tagline` if UI changed).
2. Build APK locally or use CI artifact.
3. `adb install -r` and launch on device.
4. User (or logcat) confirms the change.

## Not in scope for this fork

Desktop `cargo run -p tagline`, macOS window screenshots, and GPU desktop test matrices are upstream desktop flows — prefer Android steps above.
