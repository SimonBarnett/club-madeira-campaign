# Campaign review - The Webmaster's Hours (2026-09-21)

Hostile review of `README.md`, `AGENTS.md`, `docs/BRIEF.md`, `metrics.md`,
`episodes/_template.yaml`, and open issues FR-00 - FR-14.

Reviewed tree at `471d323`. No source PDF was supplied.

This document is the gap analysis only. Each gap below is parked as its own
`fr` issue. This review does not change the brief and does not approve any
episode.

## Verdict

The plan is a **production schedule, not a campaign**.

Production is over-specified: YAML schema, voice cast, beat structure, banned
words, ship cadence by weekday, approval gate. That part is genuinely good and
most teams never get that far.

Demand and conversion are close to unspecified. Nothing in the repo says how
anyone finds the videos, what happens when someone responds, or how you would
know at week 4 whether to keep going. Eight excellent films that nobody sees
is the same outcome as eight bad ones, at higher cost.

## P0 - the campaign cannot be judged

### 1. Attribution does not exist (FR-15)

`metrics.md` asks for per-episode "Simulator completes" and "Partner invites".
There is no UTM convention, no per-episode link, and no named analytics
property on `sim.ntsa.uk` or `clubmadeira.uk/partners`. Those columns cannot be
filled in honestly, only guessed.

This also disarms the one kill criterion in the brief ("If week 3 has no
host-flavoured comments, change the joke target"). You cannot fire a trigger
you cannot measure.

### 2. The north-star metrics have no definitions (FR-16)

"Qualified partner conversation", "host-flavoured comment", and "partner
invite" are the three numbers the campaign is graded on. None is defined.
Two people counting the same week will not get the same answer, so the
week-4 go/no-go is a matter of opinion.

### 3. The host offer has never been arithmetic-tested (FR-17)

Published economics are a sign-up fee per community plus **1% of sales** while
live. The campaign's closing episode ("Priya's recurring 1%") makes that 1%
the emotional payoff of the whole series.

Nothing in the repo models what 1% is worth to a web designer. If a club
catalogue turns over a few thousand a year, 1% is a rounding error against an
agency day rate, and a host audience will do that sum faster than we do. If
the number is small, the pitch has to lead on the sign-up fee, client
retention, and zero-maintenance revenue instead, and episode 8 needs a
different button.

This is the single highest-risk assumption in the campaign and it is currently
untested.

### 4. Funnel mismatch: odd weeks point hosts at a club artefact (FR-18)

North star is recruiting **hosts** (web designers, agencies, freelancers).
The slate sends odd weeks to `sim.ntsa.uk`, a fundraising simulator built to
persuade **club officers**. Four of eight episodes therefore send the primary
audience to an asset addressed to somebody else.

Either the simulator needs a host-facing framing, or odd weeks need a
different destination.

### 5. No inbound path (FR-19)

`AGENTS.md` correctly forbids emailing anyone who did not raise a hand. It
never says what happens when somebody **does** raise one. There is no owner,
no response time, no destination (DM, email, booked call), and no record of
the conversation. FR-11's reply bank covers wording, not routing.

## P1 - reach

### 6. No distribution plan at all (FR-20)

The repo names two platforms and a posting time and stops. It does not name
a single place hosts actually gather: web-design subreddits, Wix and WordPress
communities, agency Slacks and Discords, LinkedIn groups, Indie Hackers,
local agency meetups. Organic reach from a cold brand account is close to
zero, so without seeding the slate ships into silence.

It also never decides whether these post from a personal account or a brand
account. On both X and LinkedIn that choice is worth more than the scripts.

### 7. Six dead days a week (FR-21)

Cadence is Mon script, Tue TTS, Wed stills, Thu publish, Fri unpack, Sun
metrics. Publishing is one artefact per week. Both algorithms reward
frequency, and a feed with one post a week does not hold an audience between
episodes.

### 8. Each episode is used once (FR-22)

`episodes/_template.yaml` already has `companion.carousel_lines`, and no issue
owns it. One 60s film is at minimum: the film, a 15s hook cut, a 1:1 cut, a
carousel, a written post, a quote card, and a comment-reply asset. The slate
plans 8 assets where it could plan 50.

## P1 - risk

### 9. No affiliate-disclosure or ad-standards pass (FR-23)

This is affiliate marketing, promoted in the UK, with an episode built around
Amazon Associates. UK CAP rules on identifying marketing communications and
the Amazon Associates operating agreement both impose specific obligations,
including how the programme may be described. Nothing in the repo mentions
disclosure, and `AGENTS.md` lets an agent publish without a compliance gate.

### 10. Episode 04 pre-empts a human decision (FR-24)

Brief rule 8 says do not name Easyfundraising unless issue #13 says so, and
issue #13 is still open. `metrics.md` already lists episode 04 as
**"Easy versus on-our-site"**, which is a pun on that name, while `BRIEF.md`
and FR-05 call the same episode "on-site catalogue vs off-site portal".

Two problems in one line: the titles drift across three files, and the
published one leans on a comparison a human has not signed off.

### 11. The comedy depends on synthetic delivery, with no quality gate (FR-25)

The register is deadpan British sitcom. Deadpan is entirely timing, and
timing is the hardest thing for TTS to land. The pipeline commits to
`open-tts` with no quality bar, no listen-back gate, and no human-VO fallback
if the read is flat. A flat read does not produce a weaker joke, it produces
no joke.

### 12. Nothing enforces the rules the repo already wrote (FR-26)

There is no CI. `_template.yaml` says `named_objects` must be exactly three,
`banned` lists four phrases, `approved` must be flipped by a human, and
`AGENTS.md` forbids claims outside the brief. Every one of those is a comment,
not a check. The approval gate in particular is the thing standing between an
agent and an unreviewed public post.

## P2 - proof, access, and stopping

### 13. One nameable client, used in week 7 (FR-27)

Mereside Model Flying Club is the only real club the agent may name. The
strongest asset a host-recruitment campaign can have is another host saying it
worked, and there is no pipeline for generating or clearing more proof.

### 14. Accessibility is one word (FR-28)

Captions are required, which is a good start. There are no transcripts, no
alt text rules for quote cards and carousels, and no contrast standard, on a
campaign whose audience builds websites for a living and will notice. The repo
has an `accessibility` label with zero issues on it.

### 15. No way to stop (FR-29)

The only stopping rule is "change the joke target" at week 3. There is no
cost ceiling, no hours ceiling, no scheduled go/no-go, and no definition of
failure for the eight weeks as a whole. A campaign that cannot be cancelled
will be finished out of momentum regardless of results.

## What is already right

Worth keeping, because most of it is unusually disciplined:

- Human approval gate on publish (`approved: true`) and the `needs-human` list.
- "Punch the situation, never the treasurer" and the no-cruelty rule.
- Naming concrete artefacts, and the ban on `pyramid` / `disrupt` / `just use AI`.
- Keeping AWS internals out of the pitch.
- Capping the RPSGame easter egg at two uses and always handing the viewer back.
- A north star of conversations rather than followers.

The strategy instincts are sound. The missing half is everything after the
video renders.
