# Visual-regression candidates — v0.2.1

Eight screenshot candidates from **guardian, photo, volcanic and toon** at
1440×900 desktop and 390×844 mobile. Captured in real Chromium using
fictional/synthetic inputs. Owners must visually review and approve these
images before committing or tagging. They are *not* automatically approved
because the compare script reports 0% drift.

Use `python3 scripts/check_visual_baselines.py --screenshots private/screenshots
--tolerance 0.25` to detect unexpected change. To accept new baselines after
inspection, use `python3 scripts/update_visual_baselines.py --screenshots
private/screenshots --accept`. The visual contact sheet in the CI artifact
includes the eight original gallery worlds; browser CI checks all 11 gallery worlds, while only eight guardian/photo/volcanic/toon desktop/mobile screenshots are fixed baselines.

Pixel comparison cannot certify taste, truthful art or photo-anchor accuracy.
