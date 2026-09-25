# Legacy HOT4D scenes

Cinema 4D identifies plugin objects by numeric type, not the displayed name.
Valkaari's S24 source uses deformer 1051458 and effector 1051489. Kent's source
uses deformer 1057479 and effector 1057480. Installing only a different type's
handler does not make saved objects of the old type work.

The development build registers hidden handlers for both pairs when
`MS_OCEAN_LEGACY_COMPAT=ON` (the default). They evaluate the existing object in
place: no manual copying of settings, replacement of animation tracks, or
rewriting of object links is required by this design. Saved objects retain their
original type. New Motion Squared objects use separate development-only IDs.

All shared parameter IDs 10000–10027 match the inspected Valkaari S24 and Kent
schemas. Kent's Create Foam Tags button is 10028. Changing UI grouping must never
renumber these serialized fields. Aitidi's changed foam parameter numbering is
not adopted; scenes saved by that adaptation are not covered by these handlers.

Use this compatibility build without another HOT4D binary loaded into the same
Cinema 4D process. Already-registered legacy types are skipped, but loading two
implementations remains dependent on startup order. The original installed 2025
HOT4D is not changed by building or testing this project.

The Cinema 4D 2026.3.4 host tests pass for deformer evaluation, clone settings,
animation tracks, save/reload, and numerical parity across these three type IDs.
The new and both legacy MoGraph effectors also produce matching finite output.
See VALIDATION.md for exact scope.

A user has confirmed opening an original legacy project using Valkaari deformer
1051458 after installation and restart. Production-scene animation, rendered
appearance and save/reopen equivalence still need verification. Earlier headless
inventories missed the missing object, so they must not be used to conclude that
a scene contains no legacy data.

Pre-S24 deformer 1026624 and displacement shader 1026641 use a different schema
and are not supported. Aitidi-renumbered parameter layouts are not supported.

Permanent Maxon-issued Motion Squared IDs must replace the development-only IDs
1000001–1000003 before public release, and before creating production scenes that
must keep the new Motion Squared identity across future releases.
