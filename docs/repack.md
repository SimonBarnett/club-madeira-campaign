# Repurposing pack

Issue: [#23](https://github.com/SimonBarnett/club-madeira-campaign/issues/23)
(FR-22, review gap 8).

One episode is seven assets, not one Thursday film. `companion.carousel_lines`
already exists on `episodes/_template.yaml`; this pack owns that field.

Cuts (15s hook, 1:1) **depend on FR-08** (ffmpeg export pack). Until that
lands, mark those two checklist boxes only after a manual export.

## The seven

| # | Asset | Source | When |
|---|--------|--------|------|
| 1 | 45–75s film | `lines` + TTS/studio | Tue render |
| 2 | 15s hook cut | first beat / FR-08 | Tue export |
| 3 | 1:1 cut | same film, square | Tue export |
| 4 | LinkedIn carousel | `companion.carousel_lines` | Wed stills |
| 5 | Text-only post of the strongest beat | `repurpose.strongest_beat` | Wed |
| 6 | Quote card still | `repurpose.quote_card_line` | Wed |
| 7 | Reply asset for the predictable objection | `repurpose.reply_objection_text` | Wed; post as first reply Thu |

Do not invent a second joke for the reply. It answers the objection that
episode invites (price, "will it break Wix", "we already have a shop").

## Checklist

`episodes/_template.yaml` has a `repurpose:` block. Every episode YAML copies
it. An episode is not done — and must not flip `approved: true` — until all
seven booleans are true.

`strongest_beat`, `quote_card_line`, and `reply_objection_text` are the
copy for items 5–7. Empty strings mean those assets do not exist yet.

## Episode 01

The first Thursday that ships episode 01 must have all seven files or posts
ready, not just the film. Script YAML for episode 01 is issue #32 (do not
fork that draft here). When that YAML lands, copy the `repurpose:` block
and fill it before `approved: true`.

## Cadence fit

Mon script (including the three copy fields) → Tue film + hook + 1:1 →
Wed carousel / text / quote card / reply asset → Thu personal-first publish
(`docs/distribution.md`) → Fri unpack → Sun `metrics.md`.
