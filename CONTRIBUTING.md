# Contributing

Please report your exact Cinema 4D version, operating system, plugin version and steps to reproduce. For legacy projects, include the missing plugin ID and expected behaviour. Share only scenes you are entitled to publish; use a small reproducible scene without private assets.

Keep serialized object and parameter IDs stable. Do not replace legacy nodes or renumber fields to rearrange the interface. Changes to compatibility require host tests for settings, animation tracks, cloning and saving/reopening.

Run `python -m unittest discover -s tests -p "test_*.py"`. Native changes also require building against the target Maxon SDK and running `tests/host_smoke.py` in licensed c4dpy. CI only checks the source schema and Python syntax; it does not compile or run Cinema 4D.

Preserve upstream attribution and GPL notices. Do not commit proprietary SDK files, scene fixtures, credentials or generated binaries. Permanent Maxon-issued IDs are required before a production release.
