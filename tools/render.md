# FR-07 — open-tts render path from episode YAML

Point at [SimonBarnett/open-tts](https://github.com/SimonBarnett/open-tts). **Do not vendor** that tree into this repo.

## Prerequisites

1. Clone or install `open-tts` somewhere on the machine (sibling clone is fine).
2. `pip install -r requirements.txt` inside that repo (or install the package editable).
3. `ffmpeg` / `ffprobe` on `PATH` if you want the video mux.
4. Set **`XAI_API_KEY` in the environment** (or a local `.env` that is gitignored). Never commit keys.

```powershell
$env:XAI_API_KEY = 'your-key'   # shell only
# or: copy .env.example -> .env and export yourself
```

## Voice map

Campaign speakers → Grok TTS / open-tts `voice_id` live in [`tools/voices.yaml`](voices.yaml):

| Role | voice_id | Notes |
|------|----------|-------|
| priya | eve | placeholder until a priya sheet exists upstream |
| graham | leo | placeholder |
| chair | ara | Grok TTS id; add to open-tts `characters/registry.yaml` before video mux |
| eve | eve | direct |
| leo | leo | direct |

## Render command

From this repo root (after open-tts is importable by Python):

```powershell
python tools/render_episode.py episodes/01-example.yaml
```

What it does:

1. Reads `episodes/NN-*.yaml` (`lines[].speaker` / `text` / optional `cue`).
2. Maps speakers via `tools/voices.yaml`.
3. Writes `tools/.render-work/<slug>.open-tts.yaml` (gitignored work dir).
4. Runs `python -m open_tts render tools/.render-work/<slug>.open-tts.yaml`.

Dry-run (no API / no TTS) — useful in CI and tests:

```powershell
python tools/render_episode.py episodes/01-example.yaml --dry-run
```

If `open_tts` is only available in another interpreter:

```powershell
python tools/render_episode.py episodes/01-example.yaml --python C:\path\to\open-tts\.venv\Scripts\python.exe
```

## Studio pass

After a render, scrub / edit / re-render lines in the open-tts Qt studio:

```powershell
python -m open_tts.studio --edit tools/.render-work/<slug>.open-tts.yaml
# or: python -m open_tts.studio --edit <open-tts-output-dir>
```

Then run the listen-back comedy gate (`docs/tts-comedy-timing-gate.md`) before stills.

## Episode YAML shape (minimum)

```yaml
episode: 1
slug: example
title: "Example cold open"
approved: false
lines:
  - beat: hook
    speaker: priya
    text: "The treasurer has a spreadsheet."
    pause_before_ms: 0
    pause_after_ms: 200
  - beat: turn
    speaker: graham
    text: "Of course he does."
    cue: pause
```

Human must set `approved: true` before publish (see `AGENTS.md`).
