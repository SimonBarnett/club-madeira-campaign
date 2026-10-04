# The Webmaster's Hours

Club Madeira / Smart Catalogue comedy campaign for **X** and **LinkedIn**.

North star: recruit **hosts** — web designers, small agencies, freelancers who already look after club sites — to embed the Smart Catalogue.

This repo is the agent operating surface. Product code lives elsewhere.

## Related repos

| Repo | Role |
|---|---|
| [SimonBarnett/open-tts](https://github.com/SimonBarnett/open-tts) | Grok TTS + interview/video pipeline |
| [SimonBarnett/Madeira-Partners](https://github.com/SimonBarnett/Madeira-Partners) | What a host actually deploys |
| [SimonBarnett/affiliate-marketing](https://github.com/SimonBarnett/affiliate-marketing) | Simulator at sim.ntsa.uk |
| [SimonBarnett/RPSGame](https://github.com/SimonBarnett/RPSGame) | Easter egg only — not the product |
| [SimonBarnett/AWS](https://github.com/SimonBarnett/AWS) | Platform internals — do not lead marketing with this |

## Public URLs

- Product: https://www.thesmartcatalogue.com/
- Partners: https://www.clubmadeira.uk/partners
- Simulator: https://sim.ntsa.uk

## How an agent should work this repo

1. Read [`docs/BRIEF.md`](docs/BRIEF.md) and [`AGENTS.md`](AGENTS.md).
2. Pick the next open issue labelled `fr`.
3. Scripts live in `episodes/NN-slug.yaml`. A human must set `approved: true` before publish.
4. Keys never go in git. `XAI_API_KEY` stays in the environment.
5. Thursday is ship day. Stills + TTS counts as a finished episode.

## Render TTS (FR-07)

Episode YAML is adapted and passed to [open-tts](https://github.com/SimonBarnett/open-tts) — full command sheet in [`tools/render.md`](tools/render.md). Do not vendor open-tts into this repo.

```powershell
python tools/render_episode.py episodes/NN-slug.yaml --dry-run
python tools/render_episode.py episodes/NN-slug.yaml
python -m open_tts.studio --edit tools/.render-work/<slug>.open-tts.yaml
```

Voice map: [`tools/voices.yaml`](tools/voices.yaml). `.env` is gitignored; copy from `.env.example` if needed.

## Issue labels

- `fr` — feature request the agent can implement
- `episode` — weekly film
- `needs-human` — blocked on a decision from Simon
- `easter-egg` — RPSGame, cap two public uses in 8 weeks

## License

MIT. Same as the rest of the Club Madeira public kits.
