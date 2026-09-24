# Accessibility pack — FR-28 / issue #29

Captions were already required. This pack adds transcripts, alt text, and a
caption contrast/size rule so hosts who build sites for a living do not clock
us for skipping the basics.

## Transcripts

- One full transcript per episode: `episodes/{NN}-{slug}.transcript.md`
- Same text is the LinkedIn first comment or the LinkedIn document attach
- Template: `episodes/_transcript.md`
- Episode 01 sidecar: `episodes/01-they-asked-for-a-shop.transcript.md`

## Alt text

`episodes/_template.yaml` has `companion.alt` beside `carousel_lines`:

| Field | Use |
|---|---|
| `alt.still` | Wednesday still / 1:1 cut poster |
| `alt.quote_card` | Strongest-beat quote card |
| `alt.carousel` | One string per `carousel_lines` slide |

Empty alts = not shippable. See `AGENTS.md`.

## Caption contrast and size

Authoritative numbers live in the export pack: `tools/export.md` (FR-08 owns
the ffmpeg command line; FR-28 owns the contrast/size bar).
