# Campaign brief — The Webmaster's Hours

Full operating document for the Club Madeira / Smart Catalogue comedy campaign on X + LinkedIn.

Primary goal: recruit **hosts** (web designers, digital agencies, freelance developers, club-site maintainers) who will embed the Smart Catalogue.
Secondary goal: club officers recognise it and ask their web person for it.

## Product (do not invent new claims)

White-label, zero-stock, AI-curated affiliate fundraising shop on the club's existing site. Partner keeps the client and the brand. No setup fee, no monthly platform fee. Published partner economics: sign-up fee per community + **1% of sales** through catalogues they introduced, while live. We are not a charity. Club share + partner share.

- https://www.thesmartcatalogue.com/
- https://www.clubmadeira.uk/partners
- https://sim.ntsa.uk

Do **not** lead with AWS / Lambda. Hosts care whether it breaks Wix and whether they get paid next year.

## Comedy rules

1. Punch the situation, never the treasurer.
2. The host (Priya) is the protagonist.
3. No cruelty, politics, or culture-war bait.
4. Name concrete artefacts (the email, the spreadsheet, the mug).
5. Product is the relief, not the punchline.
6. Repeat characters: Leo, Eve, Graham, Priya, The Chair.
7. 45–75 seconds. Captions on. 15s hook + 1:1 cut.
8. Contrast off-site portals vs on-site catalogue. No smear. Do not name Easyfundraising unless issue #13 says so.
9. White-label respect: partner is the trusted local expert. We are the engine room.

Register: deadpan British sitcom. Not TikTok scream.

## Eight-week slate

Odd weeks → simulator. Even weeks → partner page.

1. They asked for a shop — sim.ntsa.uk
2. Amazon Associates at 11:47pm — how-it-works
3. The committee has thoughts — partners
4. On-site vs off-site portal — simulator (needs-human on naming)
5. White label, black coffee — partners
6. Scope creep: the musical — how-it-works (optional RPS cold open)
7. Flying club in two months (Mereside only) — product
8. Priya's recurring 1% — partner invite

## Production line

Mon script → Tue `open-tts render` + studio → Wed stills → Thu LinkedIn 07:45 UK / X midday → Fri unpack → Sun `metrics.md`.

That line is the **Thursday film**. It is not the whole public week. A feed
with one post does not hold an audience between episodes (FR-21). Fill the
dead days with offcuts from work already being done for that film. No extra
shoot, no new jokes invented for the grid.

### Weekly posting grid (FR-21)

| Day | Slot | Source (already in production) | Where |
|---|---|---|---|
| Mon | Standalone joke | One line cut from this week's script | X + LinkedIn text |
| Tue | Host problem | One pain from this brief (Wix / paid next year / white-label) | X + LinkedIn text |
| Wed | Teaser | Still or quote card from this week's episode | X + LinkedIn |
| Thu | Film | LinkedIn 07:45 UK / X midday | both |
| Fri | Unpack | What the comments actually argued about | X + LinkedIn text |
| Sun | Metrics | `metrics.md` | repo only |

Rules:

- Every Mon/Tue/Wed/Fri slot is an offcut of Thursday's film. Do not add a second production burden.
- Same comedy rules as the film. Punch the situation. One CTA. Product is the relief.
- Do not replace Thursday. Do not use RPSGame as a cadence filler.
- Draft the week's four offcuts in `docs/cadence-weekNN.md` when the script exists. Week 1: `docs/cadence-week01.md`.
- Human sets episode `approved: true` before the film. First-week cadence copy also needs a human OK before it goes live.

YAML shape: see `episodes/_template.yaml`. Human sets `approved: true` before publish. `XAI_API_KEY` never in git.

## Agent permissions

May: draft, render, caption, schedule to approved accounts, reply with facts.
Must ask: extra real clubs, ads spend, pricing beyond published 1% + sign-up fee, title/cast changes, outbound email, publish without `approved: true`.

## RPSGame

https://github.com/SimonBarnett/RPSGame — easter egg only. Max two public uses in eight weeks. Never replace Thursday. Never send the exe to hosts. Hand every viewer back to episode / sim / partner page.

## North star

Qualified partner conversations. 8 videos, ~20 host comments, ~10 sim completes, ~5 partner invites, 1–2 kits deployed. If week 3 has no host-flavoured comments, change the joke target.
