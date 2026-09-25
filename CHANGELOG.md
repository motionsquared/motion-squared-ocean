# Motion Squared Ocean development build

- Adapted deformer and MoGraph callbacks and field sampling for Cinema 4D 2026,
  incorporating Aitidi's API integration while retaining Kent's resource schema.
- Added optional legacy handlers for Valkaari S24 and Kent object IDs.
- Assigned separate resource names to legacy handlers so their parameters remain animatable.
- Preserved legacy parameter values, tag links and animation tracks in place;
  legacy objects retain their original IDs when saved.
- Added separate development-only Motion Squared creation IDs.
- Preserved all-zero weight masks and restored foam-tag undo recording.
- Moved point-selection writes out of the parallel evaluation loop.
- Guarded degenerate normalization ranges and zero loop/time-scale values.
- Updated CMake registration and isolated the simulation's module identity.

Compatibility scope is limited to verified source schemas and tested scenes.
This is not a claim that every historical HOT4D release is supported.
