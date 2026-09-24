# Feature request: Name approved personal and brand account handles

**Date:** 2026-09-22
**Repo:** https://github.com/SimonBarnett/club-madeira-campaign
**Raised by:** hostile MRB of SHA `8ae3256e4a69d1b368c3b691b5744eafc7b905fb` (PR #34 / issue #21)
**UAT + hostile MRB owner:** Bob
**Related:** issue #21 (`docs/distribution.md`), issue #14 (FR-13 bios)

Parked because SHA `8ae3256e` decides personal accounts are primary and brand
accounts are amplifier, but names no handles. An agent cannot schedule or
quote-repost from "Simon's personal accounts" without inventing them.

This is **needs-human**. Do not invent handles. Do not implement on the #21
FIX/MRB job.

No source PDF was supplied.

## Gap vs current tree

`docs/BRIEF.md` and `AGENTS.md` say "schedule to approved accounts" and never
list those accounts. FR-13 (#14) is bio + featured-link copy, not identity.
`docs/distribution.md` on PR #34 says "Simon's personal accounts on X and
LinkedIn" and "brand accounts (Club Madeira / Smart Catalogue)" with no `@`
or profile URL.

## LOCKED

- Account *decision* stays: personal primary, brand quote/amplify after.
- Do not invent handles, profile URLs, or extra real clubs.
- Do not put passwords or API keys in git.

## UNKNOWN (Simon must fill)

- Personal X handle
- Personal LinkedIn profile URL
- Brand X handle(s) allowed to quote
- Brand LinkedIn Page name(s) allowed to quote

## Deliverable

A short `docs/approved-accounts.md` (or a section Simon writes into
`docs/distribution.md`) listing only the handles Simon confirms. Empty
UNKNOWN rows until then. `needs-human` stays until the four UNKNOWN fields
are filled.

## Acceptance

| ID | Gate |
|---|---|
| H1 | The file exists and contains no invented handles. |
| H2 | Each of the four UNKNOWN fields is either a Simon-confirmed value or still marked UNKNOWN. |
| H3 | Agents are told not to post from any account not on that list. |

## Non-goals

- Changing personal-vs-brand.
- Warm-up comment logging (separate FR).
- Paid ads.
