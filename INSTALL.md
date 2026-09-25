# Private development build — Cinema 4D 2026 Windows x64

1. Extract this archive to a separate test folder.
2. Add the extracted motion-squared-ocean folder to Cinema 4D 2026's plugin search paths and restart Cinema 4D.
3. Find Motion Squared Ocean or Motion Squared Ocean Effector in Cinema 4D's command search.
4. For the deformer, place it under a subdivided editable polygon surface. Use Create Foam Tags when vertex-colour output is needed.

Use this test build without another HOT4D binary loaded into that Cinema 4D process. It registers hidden Valkaari S24 and Kent compatibility handlers, so matching old nodes can retain their existing IDs and settings.

New Motion Squared objects currently use development-only IDs. Do not use them for production scenes that must survive future releases. Permanent Maxon IDs are required before release.

This build has been tested in Cinema 4D 2026.3.4 on Windows. Older Cinema 4D versions and macOS are not covered by this package. See VALIDATION.md and COMPATIBILITY.md for the tested compatibility scope.

Corresponding GPL source is included in corresponding-source. The Maxon SDK and compiler are separate build dependencies.
