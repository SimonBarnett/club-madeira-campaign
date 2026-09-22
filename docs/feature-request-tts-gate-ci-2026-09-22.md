# Feature request — CI for TTS comedy-timing gate validator

Parked 2026-09-22 from MRB of FR-25 / [#26](https://github.com/SimonBarnett/club-madeira-campaign/issues/26) at SHA `45ff51a4740d520a7bb84b18bf9823135a003d94`.

No source PDF was supplied.

This is intake only. Do not implement in the FR-25 MRB job.

## Gap vs current tree

FR-25 ships `tools/validate_tts_gate.py`, `episodes/gates/_template.yaml`, and (on that PR) authored timing rules. `main` already has `.github/workflows/episodes-ci.yml` (FR-26 / #27, merged via PR #33). That Action runs `tools/validate_episodes.py` and `tools/publish_guard.py` only. It does **not** run the TTS gate validator.

A validator that is never run on PR/push will rot. Isolated probes on the FR-25 SHA show the line-timing and pass-check branches work, but there is no in-repo broken fixture and no CI step.

## LOCKED

- Listen-back checks stay the three in `docs/tts-comedy-timing-gate.md`: `button_lands`, `pause_before_turn_ok`, `stranger_would_laugh`.
- `verdict: pass` requires all three `true`.
- Turn lines: `pause_before_ms >= 400`. Button lines: `pause_after_ms >= 500`.
- Two written fails trigger human VO for Priya (`fallback_triggered` + `fallback_reason`).
- No secrets in git. `XAI_API_KEY` stays in the environment.
- Do not replace Thursday's episode. Do not weaken FR-26 episode-schema CI.

## UNKNOWN

- Whether `episodes/gates/ep01-example-fallback.yaml` (shape-only) stays under `episodes/gates/` or moves to `fixtures/gates/` so operational scans cannot treat it as a real episode-01 double-fail.
- Whether the Action is a new job or a step on `episode-yaml-ci`.

## Acceptance

- [ ] A1. GitHub Action on PR and push runs `python tools/validate_tts_gate.py` and is green on the gate template plus any honest pass fixture.
- [ ] A2. A deliberately broken fixture fails (at least: `verdict: pass` with a false check, and a turn line with `pause_before_ms < 400`).
- [ ] A3. Existing `validate_episodes.py` / publish-guard steps stay green. This FR does not reopen #27.

## Out of scope

Rebasing PR #38. Writing episode 01. FR-07 open-tts render. Human VO recording.
