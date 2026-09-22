# Feature request: refuse `approved: true` on an incomplete seven-asset pack

Parked from MRB of [FR-22 / #23](https://github.com/SimonBarnett/club-madeira-campaign/issues/23)
at SHA `6caa6fcb288244bbdfe42a48c96776178de59ea8`. No source PDF was supplied.

This is **not** a second copy of FR-22. FR-22 added the `repurpose:` checklist.
This request owns the **gate**: an episode must not be markable or schedulable
as approved while any pack boolean is still false.

May land as an extra check inside [FR-26 / #27](https://github.com/SimonBarnett/club-madeira-campaign/issues/27)
rather than a second GitHub Action. #27's parked deliverable list does not
name this conjunction.

## Gap vs current tree

After #23 / PR 35:

- `docs/repack.md` and `docs/BRIEF.md` say do not flip `approved: true` until
  all seven `repurpose` booleans are true.
- `episodes/_template.yaml` has the seven booleans and three copy strings.
- Nothing fails a YAML that sets `approved: true` with every boolean still
  `false`, or a boolean `true` with its copy string still empty.
- `README.md` still says "Stills + TTS counts as a finished episode".
- `AGENTS.md` still treats `approved: true` alone as the publish gate.
- FR-26 (#27) lists schema, banned phrases, length, CTA, disclosure, title
  drift, secrets, and "refuse to schedule if `approved` is not true". It does
  **not** list `approved: true` ⇒ pack complete.

## LOCKED

- Pack booleans: `film_45_75s`, `hook_15s`, `cut_1_1`, `linkedin_carousel`,
  `text_only_strongest_beat`, `quote_card_still`, `reply_objection`.
- Copy fields for items 5–7: `strongest_beat`, `quote_card_line`,
  `reply_objection_text`. Empty string means that asset does not exist.
- `approved: true` is illegal unless all seven booleans are true.
- A true boolean with an empty paired copy field is illegal.
- Hook and 1:1 may stay false until [FR-08 / #9](https://github.com/SimonBarnett/club-madeira-campaign/issues/9)
  lands. That means `approved` stays false. Do not invent a bypass.
- `XAI_API_KEY` and passwords stay out of git.

## UNKNOWN

- Whether the check lives in the FR-26 Action, a publish-time script, or both.
- Whether episode 01 YAML (#3 / #32) exists when this lands.

## Acceptance

- [ ] A-1: CI or publish guard fails when `approved: true` and any of the
      seven booleans is false.
- [ ] A-2: CI or publish guard fails when
      `text_only_strongest_beat` / `quote_card_still` / `reply_objection` is
      true and the paired copy string is empty.
- [ ] A-3: `_template.yaml` as shipped (`approved: false`, all booleans
      false, empty copy) still passes.
- [ ] A-4: No secrets in repo or fixtures.

Do not implement this inside the FR-22 pack PR.
