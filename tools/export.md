# FR-08 ffmpeg export pack

Issue: [#9](https://github.com/SimonBarnett/club-madeira-campaign/issues/9)

Per episode, produce four publish-ready cuts from the Tue TTS/studio master (no media binaries in git):

| Output | Size / length | Use |
|--------|----------------|-----|
| Feed 9:16 | 1080×1920 | X / Reels-style |
| LinkedIn-safe 1:1 | 1080×1080 | LinkedIn native |
| Hook | first **15s** of the film (same aspect as feed unless `--hook-square`) | Cold open / ads |
| Captions | **burned in** on every cut (clubs watch in the kitchen with sound off) | All of the above |

Cuts feed the seven-asset pack in [`docs/repack.md`](../docs/repack.md) (items 2–3).

## Inputs

| Arg / path | Meaning |
|------------|---------|
| `--master` | Master episode video (from FR-07 / open-tts), any reasonable aspect |
| `--captions` | `.srt` or `.ass` sidecar (UTF-8). Required for burn-in |
| `--out-dir` | Output directory (default `exports/<slug>/`, gitignored) |
| `--slug` | Episode slug for file names (e.g. `01-they-asked-for-a-shop`) |
| `--hook-seconds` | Hook length (default `15`) |

Do **not** commit `exports/`, `*.mp4`, or rendered stills. Same rule as open-tts interview outputs.

## Driver

```text
python tools/export_episode.py --master path/to/master.mp4 --captions path/to/ep.srt --slug 01-they-asked-for-a-shop --dry-run
python tools/export_episode.py --master path/to/master.mp4 --captions path/to/ep.srt --slug 01-they-asked-for-a-shop
```

`--dry-run` prints the ffmpeg command lines and exits 0 without calling ffmpeg. Useful on seats without ffmpeg and in CI.

Requires `ffmpeg` + `ffprobe` on `PATH` for a real export. Escape caption paths for the `subtitles=` filter (Windows backslashes → forward slashes; `:` escaped).

## Example filter graphs

9:16 feed with burned captions:

```text
scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,subtitles=CAPTIONS
```

1:1 LinkedIn-safe:

```text
scale=1080:1080:force_original_aspect_ratio=increase,crop=1080:1080,subtitles=CAPTIONS
```

15s hook (feed aspect): same 9:16 graph with `-ss 0 -t 15` before `-i` (input seek) or after (accurate). The script uses accurate seek after `-i` so captions stay aligned.

## Week 1 example run

Blocked until:

- FR-02 / issue #3 — week 1 script YAML
- FR-07 / issue #8 — open-tts render path from episode YAML

When those land, render week 1 audio/video + `.srt`, then:

```text
python tools/export_episode.py --master exports/work/01-master.mp4 --captions exports/work/01.srt --slug 01-they-asked-for-a-shop
```

Flip `repurpose.hook_15s` and `repurpose.cut_1_1` in the episode YAML only after the files exist on disk (still never commit the binaries).

## Tests

```text
python -m unittest tools.test_export_episode -v
```

Covers argv construction, caption-path escaping, and refusal to write under the repo without an explicit `--out-dir` outside git when `--require-outside-repo` is set (default off; docs warn).
