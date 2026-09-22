# FR: Accessibility publish gate (transcript sidecar + companion.alt)

**Repo:** SimonBarnett/club-madeira-campaign  
**Date:** 2026-09-22  
**Labels:** `fr`, `accessibility`, `pipeline`  
**Parent:** issue #29 / FR-28 (accessibility pack). Adjacent to issue #27 / FR-26 (YAML CI).  
**Source PDF:** none supplied.

## Summary

FR-28 makes an episode unshippable without a transcript sidecar and filled
`companion.alt`. That rule is a comment in `AGENTS.md`. Nothing fails a PR or
blocks publish when the sidecar is missing, empty, drifted from `lines:`, or
when `companion.alt` is blank.

FR-26 / PR #33 checks YAML schema, banned phrases, CTA URLs, titles, and
secret-shaped strings. It does not check transcript files or alt text.

## Gap vs current tree

At `471d323` (main) there is no a11y pack. At PR #36 head `eee8d8b` the pack
lands (`companion.alt`, `episodes/*.transcript.md`, `tools/export.md` contrast
bar, `AGENTS.md` ship line). After that merge the gate is still prose.

Open issue #27 does not list these checks in its deliverable. Do not treat this
as a second copy of FR-28 (templates and the ep01 sidecar stay on #29).

## LOCKED

- Transcript path: `episodes/{NN}-{slug}.transcript.md` next to the YAML.
- `companion.alt.still`, `companion.alt.quote_card`, and `companion.alt.carousel[]`
  one-for-one with `companion.carousel_lines`.
- Empty alts or a missing sidecar = not shippable. `approved: true` does not override.
- No secrets in git (`XAI_API_KEY`, `password=`).
- Do not invent product claims beyond `docs/BRIEF.md`.

## UNKNOWN

- Whether the check lives in FR-26's `tools/validate_episodes.py` or a sibling script.
- Whether publish-time (`tools/publish_guard.py`) or PR CI is the one hard fail.

## Acceptance

| ID | Gate |
|---|---|
| A1 | CI fails a fixture episode YAML whose `companion.alt` still/quote/carousel is empty. |
| A2 | CI fails when `episodes/{NN}-{slug}.yaml` exists and `episodes/{NN}-{slug}.transcript.md` does not. |
| A3 | CI fails when the transcript spoken text does not cover the YAML `lines:` (drift). |
| A4 | Template `episode: 0` / `slug: template` stays exempt, same as FR-26. |
| A5 | No media binaries committed. No secret assignments in git. |

## Out of scope

- Authoring episode 01 dialogue (issue #3 / FR-02).
- ffmpeg burned-caption CLI (issue #9 / FR-08).
- Caption contrast numbers (already on #29 / `tools/export.md`).
