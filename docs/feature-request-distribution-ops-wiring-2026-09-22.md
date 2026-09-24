# Feature request: Distribution ops wiring (load-first + warm-up log)

**Date:** 2026-09-22
**Repo:** https://github.com/SimonBarnett/club-madeira-campaign
**Raised by:** hostile MRB of SHA `8ae3256e4a69d1b368c3b691b5744eafc7b905fb` (PR #34 / issue #21)
**UAT + hostile MRB owner:** Bob
**Related:** issue #21 (`docs/distribution.md`), issue #15 (FR-14 Sunday metrics fill),
issue #17 (FR-16 metric definitions)

Parked because SHA `8ae3256e` added a distribution plan that agents will not
load and a warm-up count that `metrics.md` cannot hold. Those holes are
**not** acceptance of #21. Do not implement on the #21 FIX/MRB job.

No source PDF was supplied.

## Gap vs current tree

`AGENTS.md` load-first is `docs/BRIEF.md`, open `fr` issues, and `episodes/`.
`README.md` "How an agent should work this repo" repeats that list.
Neither file names `docs/distribution.md`. An agent that follows the written
load path will miss the account decision (personal primary, brand amplifier)
and the participate-vs-post table.

`docs/distribution.md` (on PR #34, not yet on `main` at park time) requires:

- Log warm-up comment **count** (not text) in `metrics.md` on Sunday.
- Launch bar: at least five table rows with a logged participate-week
  (comment count > 0), including one Wix-or-WordPress place and one
  freelance/agency place.

`metrics.md` columns today are: Week ending, Episode, Host comments,
Simulator completes, Partner invites, Notes. There is no warm-up column and
no per-community participate-week log. FR-14 (#15) fills the existing row
after Thursday ship. FR-16 (#17) defines north-star metrics only. Warm-up
comments are explicitly not the north star.

## LOCKED

- North star stays qualified partner conversations (`docs/BRIEF.md`).
- Do not invent extra real clubs, Discords, or Slacks.
- Do not put secrets in git.
- Do not change the #21 distribution decision in this FR.

## UNKNOWN

- Personal and brand account handles (separate needs-human FR).

## Deliverable

1. `AGENTS.md` and `README.md` load-first / agent-workflow lists include
   `docs/distribution.md` next to `docs/BRIEF.md`.
2. `metrics.md` can record, without inventing numbers:
   - weekly warm-up comment **count** (pre-episode-01 weeks included)
   - which table-row communities had comment count > 0 that week
3. One sentence in `docs/distribution.md` pointing at the new log shape
   (only if `docs/distribution.md` is already on the branch; do not re-litigate
   the account decision).

## Acceptance

| ID | Gate |
|---|---|
| D1 | An agent reading only `AGENTS.md` + `README.md` is told to open `docs/distribution.md` before posting or commenting in host communities. |
| D2 | `metrics.md` has a documented place for warm-up count and participate-week ticks. Empty cells are allowed. No fabricated counts. |
| D3 | FR-14 and FR-16 remain the owners of Thursday fill and north-star definitions. This FR does not redefine those metrics. |

## Non-goals

- Naming X / LinkedIn handles.
- Joining LinkedIn groups or Discords.
- Changing personal-vs-brand.
- Implementing the warm-up comments themselves.
