# TTS comedy-timing quality gate (FR-25 / #26)

Deadpan British sitcom lives on timing. A flat `open-tts` read does not
weaken the joke — it deletes it. This gate sits **after** Tue TTS render and
**before** Wed stills.

Depends on FR-07 (open-tts render path from episode YAML). Until FR-07 ships,
agents still author markers and fill gate records; they do not skip to stills
on an ungated render.

## Listen-back checklist (written)

Fill one record under `episodes/gates/` per render attempt (see
`episodes/gates/_template.yaml`). Three questions — all must be **yes** to
pass:

1. **Button lands** — after the final line, is there enough air that the
   button feels placed, not rushed into credits/CTA?
2. **Pause before the turn** — is the silence (or breath) before the turn
   beat long enough that the turn can land?
3. **Stranger would laugh** — would someone who does not know the cast get
   the joke from the audio alone?

Optional notes: which line felt flat, which pause was short, which word
needed emphasis.

## Authored timing in YAML `lines`

Do not hope the model pauses correctly. Mark it:

| Field | Meaning |
|---|---|
| `beat` | `hook` \| `escalation` \| `turn` \| `button` |
| `pause_before_ms` | Silence before this line starts (ms) |
| `pause_after_ms` | Silence after this line ends (ms) |
| `emphasis` | List of substrings in `text` to stress |
| `cue` | Optional open-tts cue (`pause`, expression ids) |

Rules of thumb for deadpan:

- Before **turn**: `pause_before_ms` ≥ 400
- After **button**: `pause_after_ms` ≥ 500
- Prefer one clear breath over stuffing `…` into the text

Schema example lives in `episodes/_template.yaml`.

## Fallback — human VO

If the same episode fails the written gate **twice** (two render attempts,
both `verdict: fail`):

- Trigger **human VO for the protagonist** (Priya) at minimum.
- Other cast may stay synthetic if their lines already passed.
- Record `fallback_triggered: true` and `fallback_reason` on the gate file.
- Stills may proceed only after the human VO pass (or a third synthetic
  attempt that passes — do not loop forever; prefer fallback).

Named path: replace Priya's WAV/segment in the open-tts project with a
human take; keep YAML `speaker: priya` so captions/schedule stay stable.

## Format decision rule (episodes 01 and 02)

If **both** episode 01 and episode 02 fail the gate (each after two
attempts, fallback either refused or also fails the laugh test):

- **Stop** before episode 03 production.
- Change the format (register, cast density, or drop TTS-led comedy) —
  do not discover this at week 8.
- Park a needs-human issue summarizing both gate files.

## Done when

Episode 01 has a gate record with `verdict: pass`, **or** a gate record
with `fallback_triggered: true` on purpose after two fails. Until episode
01 exists on `main`, shipping this doc + template + validator satisfies
the machinery; the first real pass/fallback closes the operational loop.
