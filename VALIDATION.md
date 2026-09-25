# Validation — 25 September 2026

Built with Clang 19.1.5 and the installed Cinema 4D 2026 SDK on Windows x64. Runtime host: Cinema 4D 2026.3.4 (2026304).

All 37 checks in tests/host_smoke.py passed:

- New, Valkaari S24 and Kent deformer registrations, nonzero finite waves, clone settings and animatable descriptions.
- Save/reload preserves each original type, wave height, seed and animation track.
- All three deformer types produce identical geometry with identical settings.
- Zero vertex-map weights preserve the original mesh; zero loop and speed values stay finite.
- The foam button creates and links two vertex-colour tags and reuses them on repeat.
- New and both legacy MoGraph effectors produce finite waves on an actual Cloner, with identical output across types.

The historical parameter-schema regression also passes. These checks do not establish pixel-identical results against the old compiled HOT4D engines, field falloff equivalence, foam playback equivalence, or compatibility with every historical release.

## Legacy project status

A user has confirmed that a legacy project opens successfully in the Cinema 4D 2026 GUI after installing this build and restarting the application. Its missing plugin was Valkaari deformer ID 1051458.

Earlier headless inventories failed to expose that missing object. Those inventories are not evidence that the file contained no HOT4D data. Visual equivalence, animation playback and a save/reopen round trip of that original production project remain unverified. Private scenes and diagnostic inventories are not included in this repository.

## Build environment

Parallel compiler attempts crashed inside SDK compilation. A single-worker Clang build completed successfully. scripts/run_build.py normalizes the Windows environment, disables persistent compiler workers, and prevents child crash dialogs. The default build uses one worker.
