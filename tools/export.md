# Export pack

FR-08 / issue #9 owns the ffmpeg command line (9:16, 1:1, 15s hook, burned
captions). Do not commit media binaries. This file is the pack the encoder
must honour.

## Caption contrast and minimum size (FR-28 / issue #29)

Kitchen TVs, sound off, club-committee viewing. Hosts build websites; they
will notice a thin grey caption.

| Rule | Minimum |
|---|---|
| Contrast | WCAG 2.1 AA: **4.5:1** caption text vs its immediate background |
| Large type | **3:1** only if the caption is ≥ 24 CSS px equivalent *and* bold |
| 1080×1920 feed | Caption **42 px** or larger; max ~12 words per card |
| 1080×1080 cut | Caption **28 px** or larger |
| 15s hook | Same size as the parent cut; do not shrink for the hook |
| Fill | White (`#FFFFFF`) or off-white (`#F5F5F5`) |
| Legibility plate | Solid or ≥ 80% black box **or** a 4 px black stroke; never bare white-on-scene |
| Safe area | Keep captions inside the centre 80% width; above the CTA bug |

Measure contrast on the **composited** frame (text + plate), not the raw
fill vs the video underneath.

## Outputs (FR-08)

- 1080×1920 feed
- 1080×1080 LinkedIn-safe
- 15s hook cut
- Captions burned in to the standard above

ffmpeg recipe lands when FR-08 is implemented. Until then, any export must
still meet the contrast/size bar or it is not shippable.
