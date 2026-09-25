# Motion Squared Ocean

An open-source ocean deformer and MoGraph effector for **Cinema 4D 2026**, based on HOT4D. This fork focuses on modern SDK support and preserving existing HOT4D scenes.

**Status: experimental development build.** Tested on Windows x64 with Cinema 4D 2026.3.4. New Motion Squared objects currently use temporary development IDs; permanent Maxon-issued IDs are required before a production release.

## What it does

- Generates animated ocean deformation and MoGraph motion.
- Recognises Valkaari S24 and Kent HOT4D object identities without manually replacing nodes.
- Keeps historical parameter IDs, settings and animation tracks intact.
- Provides vertex-colour foam/Jacobian tags and vertex-map masking.

## Legacy compatibility

| Origin | Deformer ID | Effector ID | Support |
| --- | --- | --- | --- |
| Valkaari S24 | 1051458 | 1051489 | Compatibility handlers tested |
| Kent HOT4D | 1057479 | 1057480 | Compatibility handlers tested |
| Pre-S24 Valkaari | 1026624 | — | Not supported; older shader also differs |

All 37 host regression checks pass, covering deformation, animation tracks, clone settings, saving/reopening, masks, foam-tag creation and MoGraph output. A user has also confirmed that a legacy project opens after installing this build and restarting Cinema 4D. Matching the original rendered appearance and production-scene round trips still need verification.

See [compatibility](COMPATIBILITY.md) and [validation](VALIDATION.md) for the precise scope. Aitidi-renumbered scene parameters are not covered. Load only one HOT4D implementation in a Cinema 4D process to avoid ID collisions.

## Build and install

You need the Cinema 4D 2026 SDK, Visual Studio 2022 Build Tools with ClangCL and CMake, Windows SDK 10.0.20348.0, and Python 3. The proprietary Maxon SDK is a separate dependency and is not included.

```powershell
python scripts/run_build.py -SdkRoot 'C:/path/to/c4d-sdk-2026'
```

CMake and Python must be on PATH, or pass `-CMake` and `-Python` with their executable paths. Use `-CinemaExecutable` for a non-default Cinema 4D location. The build defaults to one compiler worker and writes the plugin to `build/ClangCL/bin/Release/plugins/motion-squared-ocean`.

Copy that plugin folder into the **plugins** directory of your Cinema 4D 2026 user preferences folder and restart Cinema 4D. Search for **Motion Squared Ocean** or **Motion Squared Ocean Effector**. See [installation notes](INSTALL.md).

Keep original projects untouched and test with copies. Do not use the temporary new-object IDs in production projects that need a stable identity across future releases.

## Tests

```powershell
python -m unittest discover -s tests -p "test_*.py"
python scripts/run_host_tests.py --modules build/ClangCL/bin/Release/plugins
```

The second command needs licensed Cinema 4D c4dpy. GitHub Actions checks source schemas and Python syntax only; it does not compile or execute Cinema 4D. Private scene fixtures and generated test results are excluded from Git.

## Credits and licence

Distributed under [GNU GPL v2](LICENSE.txt). This is a derivative project, not an original ocean algorithm or an official Maxon product.

- [Drew Whitehouse](https://github.com/eloop/hot): Houdini Ocean Toolkit.
- [Manuel Magalhaes / Valkaari](https://github.com/Valkaari/HOT4D): original Cinema 4D port.
- [Kent Barber / GameLogicDesign](https://github.com/kentbarber/HOT4D): the baseline used by this fork.
- [Aitidi and contributors](https://github.com/Aitidi/HOT4D-C4D2026Plus): selected Cinema 4D 2026 API adaptations.
- Motion Squared: modern build integration, compatibility handlers and fixes documented in [the changelog](CHANGELOG.md).

See [third-party notices](THIRD-PARTY-NOTICES.md) and [contributing](CONTRIBUTING.md).
