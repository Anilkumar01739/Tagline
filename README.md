# TagLine for Android

[![Android APK](https://github.com/Anilkumar01739/Tagline/actions/workflows/android-apk.yml/badge.svg)](https://github.com/Anilkumar01739/Tagline/actions/workflows/android-apk.yml)
[![License: AGPL-3.0](https://img.shields.io/github/license/Anilkumar01739/Tagline)](LICENSE)

**TagLine** is a local-first mobile video editor: multi-track timeline, effects, text and captions, and export on device—without uploading your footage to the cloud.

Maintained by [**Anilkumar01739**](https://github.com/Anilkumar01739). Package name: `app.tagline.editor`.

---

## Features

- **On-device editing** — projects and media stay on your phone or tablet  
- **Timeline** — lanes, trims, transitions, and preview  
- **Effects & color** — built-in effect packages and grading controls  
- **Text & captions** — titles and speech-to-text workflows (models download when needed)  
- **Export** — render finished videos locally  

---

## Get the app

### From GitHub Actions (recommended)

1. Open [**Android APK**](https://github.com/Anilkumar01739/Tagline/actions/workflows/android-apk.yml)  
2. Select the latest successful run on `main`  
3. Download the **`TagLine-android-arm64`** artifact  
4. Install on a **64-bit ARM** device:

   ```bash
   adb install -r TagLine-*-android-arm64.apk
   ```

To trigger a fresh build: **Actions → Android APK → Run workflow**.

### Build on your machine (Windows)

Prerequisites: Android SDK/NDK, JDK, Rust, FFmpeg cross-built for Android (see `src/README.md`).

```powershell
.\scripts\build-android-windows.ps1
adb install -r .\TagLine-debug.apk
```

---

## Repository layout

| Path | Purpose |
|------|---------|
| `src/crates/tagline` | Editor UI (Slint) and engine integration |
| `src/crates/tagline-android` | Android activity and APK packaging |
| `src/crates/tagline-*` | Media, effects, export, speech, and related libraries |
| `.github/workflows/android-apk.yml` | Linux CI that produces the arm64 APK |

---

## Licence and attribution

This project is licensed under **[AGPL-3.0-or-later](LICENSE)**.

Engine and UI code are derived from **[Concat](https://github.com/jub0t/Concat)** (AGPL). This repository is an **independent Android-focused fork**; it is not an official Concat desktop or upstream TagLine release.

- **Issues & feedback:** [GitHub Issues](https://github.com/Anilkumar01739/Tagline/issues)  
- **Branding:** [TRADEMARK.md](TRADEMARK.md)  
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
