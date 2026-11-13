# TagLine (Android)

Android-only video editor maintained by [**Anilkumar01739**](https://github.com/Anilkumar01739). Edit on your phone or tablet: timeline, effects, text, captions, local export. No cloud upload required for editing.

**Repo:** [github.com/Anilkumar01739/Tagline](https://github.com/Anilkumar01739/Tagline) · **Licence:** [AGPL-3.0-or-later](LICENSE)

## Build & install

```powershell
.\scripts\build-android-windows.ps1
adb install -r path\to\app-tagline-editor-….apk
```

CI artifact (when enabled): `TagLine-android-arm64` from **Build for phones**.

## Source layout

- `src/crates/tagline` — editor UI  
- `src/crates/tagline-android` — Android package `app.tagline.editor`  
- `docs/TAGLINE-REBRAND.md` — fork notes  

## Attribution

Engine code is derived from [Concat](https://github.com/jub0t/Concat) (AGPL). This repository is an independent Android-focused fork, not an official Concat/TagLine desktop release.

**Issues:** [GitHub Issues](https://github.com/Anilkumar01739/Tagline/issues) · **Trademark:** [TRADEMARK.md](TRADEMARK.md)
