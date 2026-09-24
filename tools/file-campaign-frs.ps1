# Files FR-15 .. FR-29 from the 2026-09-21 campaign review as GitHub issues.
# Requires an authenticated gh (gh auth login) or GH_TOKEN in the environment.
# Idempotent: skips any FR whose title already exists as an open issue.
[CmdletBinding()]
param(
    [string]$Repo = 'SimonBarnett/club-madeira-campaign',
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'

$gh = @(
    (Join-Path $env:LOCALAPPDATA 'GitHubCLI\gh.exe'),
    (Join-Path ${env:ProgramFiles} 'GitHub CLI\gh.exe')
) | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $gh) { $gh = (Get-Command gh -ErrorAction SilentlyContinue).Source }
if (-not $gh) { throw 'gh.exe not found' }

$review = 'docs/campaign-review-2026-09-21.md'
$reviewUrl = "https://github.com/$Repo/blob/main/$review"

$frs = @(
    @{
        title  = 'FR-15 Attribution scheme: UTM convention + per-episode links'
        labels = 'fr'
        body   = @'
**Review:** {0} (P0, gap 1)

`metrics.md` asks for per-episode "Simulator completes" and "Partner invites".
There is no UTM convention, no per-episode link, and no named analytics
property. Those columns cannot be filled in honestly today, only guessed.

This also disarms the brief's only kill criterion ("if week 3 has no
host-flavoured comments, change the joke target") - you cannot fire a trigger
you cannot measure.

### Deliverable

- `docs/attribution.md` with a locked UTM convention, e.g.
  `?utm_source=linkedin|x&utm_medium=organic&utm_campaign=webmasters-hours&utm_content=ep-NN-slug`.
- One short link per episode per platform, so LinkedIn and X are separable.
- Named analytics property and the exact event that counts as a
  "simulator complete" on sim.ntsa.uk.
- New `links:` block in `episodes/_template.yaml` holding the built URLs.
- `metrics.md` gains a "How each column is sourced" note.

### Done when

Episode 01 ships with tagged links and week 1 of `metrics.md` is filled from
analytics rather than from memory.
'@
    },
    @{
        title  = 'FR-16 Define the north-star metrics before week 1'
        labels = 'fr'
        body   = @'
**Review:** {0} (P0, gap 2)

"Qualified partner conversation", "host-flavoured comment", and "partner
invite" are the three numbers the campaign is graded on, and none is defined.
Two people counting the same week will not agree, so the week-4 go/no-go is
currently a matter of opinion.

### Deliverable

`docs/metric-definitions.md` giving, for each metric: a one-line definition,
an inclusion rule, an exclusion rule, and two worked examples (one that counts,
one that does not).

Suggested starting point, to be argued with:

- **Host-flavoured comment** - a public comment from an account whose bio or
  history shows they build or maintain websites for other people. Excludes
  club officers, excludes generic praise with no host signal.
- **Qualified partner conversation** - a two-way exchange with a host who has
  stated they maintain at least one club or community site. Excludes one-line
  replies and anything we initiated cold.
- **Partner invite** - we sent the partner page to a named host who asked for
  it, logged with date and source episode.

### Done when

The definitions are committed and `metrics.md` links to them.
'@
    },
    @{
        title  = 'FR-17 Pressure-test the host offer arithmetic (1% + sign-up fee)'
        labels = 'fr,needs-human'
        body   = @'
**Review:** {0} (P0, gap 3)

Highest-risk untested assumption in the campaign.

Published economics are a sign-up fee per community plus **1% of sales while
live**. Episode 8 ("Priya's recurring 1%") makes that 1% the emotional payoff
of the entire series. Nothing in the repo models what 1% is actually worth to
a web designer.

If a club catalogue turns over a few thousand a year, 1% is a rounding error
against an agency day rate. A host audience will do that sum faster than we
will, and in public, under our own video.

### Deliverable

- `docs/host-economics.md` modelling low / mid / high club turnover, showing
  annual host revenue per club and at 5, 10, and 25 clubs.
- An explicit answer to: at what club count does this beat one day of agency
  work per year?
- If the number is weak, a revised lead for the host pitch - sign-up fee,
  client retention, zero-maintenance recurring revenue, competitive
  differentiation when pitching club work - and a rewritten button for
  episode 8.

### Needs human

Simon to confirm real or expected catalogue turnover. Do not publish modelled
figures as fact, and do not invent numbers for a public asset.

### Done when

The model is committed and episode 8's CTA is either confirmed or replaced.
'@
    },
    @{
        title  = 'FR-18 Fix the funnel mismatch on odd weeks (host vs club assets)'
        labels = 'fr'
        body   = @'
**Review:** {0} (P0, gap 4)

North star is recruiting **hosts** - web designers, agencies, freelancers.
The slate sends odd weeks to `sim.ntsa.uk`, a fundraising simulator built to
persuade **club officers**. Four of eight episodes send the primary audience
to an asset addressed to somebody else.

### Deliverable

Pick one and write it down:

1. **Host framing on the simulator** - an entry point that shows a host what
   their client sees and what the host earns, not just what the club raises; or
2. **Re-route odd weeks** to a host-facing destination and keep the simulator
   for club-officer-flavoured episodes.

Then add a CTA routing table to `docs/BRIEF.md`: episode -> audience ->
destination -> what that page must prove.

### Done when

Every episode's `cta_url` can be justified by the audience that episode is
written for.
'@
    },
    @{
        title  = 'FR-19 Inbound routing and response SLA for raised hands'
        labels = 'fr,needs-human'
        body   = @'
**Review:** {0} (P0, gap 5)

`AGENTS.md` correctly forbids emailing anyone who did not raise a hand. It
never says what happens when somebody **does**. There is no owner, no response
time, no destination, and no record. FR-11's reply bank covers wording, not
routing.

### Deliverable

`docs/inbound.md` covering:

- Named owner per channel (LinkedIn comments, LinkedIn DM, X replies, X DM).
- Target first response time, and what the agent may send unaided vs what
  waits for a human.
- The destination: DM thread, email, or booked call - pick one primary.
- Where the conversation is logged so `metrics.md` "partner invites" has a
  source of truth.
- An explicit out-of-hours and holiday answer, since publish is Thursday and
  most replies land Thursday evening.

### Needs human

Owner and response-time commitment are Simon's call.
'@
    },
    @{
        title  = 'FR-20 Distribution and seeding plan (where hosts actually are)'
        labels = 'fr'
        body   = @'
**Review:** {0} (P1, gap 6)

The repo names two platforms and a posting time, then stops. It names no place
hosts actually gather, and never decides whether posts come from a personal or
a brand account. On both X and LinkedIn that single choice is worth more than
the scripts.

Organic reach from a cold brand account is close to zero. Without seeding, the
slate ships into silence and the week-3 kill criterion fires for the wrong
reason - not a bad joke, just no audience.

### Deliverable

`docs/distribution.md` with:

- Account decision: personal (Simon) as primary, brand as amplifier, or the
  reverse - with the reasoning.
- A named list of 10-15 communities where club-site maintainers gather:
  web-design and freelance subreddits, Wix and WordPress community forums,
  agency Slacks and Discords, LinkedIn groups, Indie Hackers, local agency
  meetups.
- The rule for each: are we allowed to post, or only to participate? Self
  promotion rules differ per community and breaking them costs the account.
- A pre-publish warm-up: 20-30 genuine comments per week on other people's
  posts in the target niche, starting **before** episode 01.
- A tagging and mention plan that does not read as spam.

### Done when

Episode 01 launches into an audience that already exists rather than an empty
room.
'@
    },
    @{
        title  = 'FR-21 Between-episode cadence (kill the six dead days)'
        labels = 'fr'
        body   = @'
**Review:** {0} (P1, gap 7)

Cadence is Mon script, Tue TTS, Wed stills, Thu publish, Fri unpack, Sun
metrics. That is one public artefact per week. Both algorithms reward
frequency, and a feed with one post a week does not hold an audience between
episodes.

### Deliverable

A weekly posting grid in `docs/BRIEF.md` that fills Mon-Wed and Fri with
low-cost, in-voice posts drawn from work already being done:

- Mon: a line cut from this week's script, posted as a standalone joke.
- Tue: a short text post on one host problem from the brief.
- Wed: a still or quote card from the episode as a teaser.
- Fri: the unpack - what the comments argued about.

No new production burden: every slot is offcuts from the Thursday film.

### Done when

The grid is committed and week 1 runs it end to end.
'@
    },
    @{
        title  = 'FR-22 Repurposing pack: one episode becomes seven assets'
        labels = 'fr,pipeline'
        body   = @'
**Review:** {0} (P1, gap 8)

`episodes/_template.yaml` already has `companion.carousel_lines` and no issue
owns it. The slate plans 8 assets where it could plan 50.

Depends on FR-08 (ffmpeg export pack) for the cuts.

### Deliverable

Per episode, a defined pack:

1. The 45-75s film.
2. 15s hook cut.
3. 1:1 cut.
4. LinkedIn carousel from `carousel_lines`.
5. Text-only post of the strongest beat.
6. Quote card still.
7. A reply asset for the predictable objection that episode invites.

Add a `repurpose:` checklist block to `episodes/_template.yaml` so an episode
is not "done" until the pack exists.

### Done when

Episode 01 ships all seven and the checklist is in the template.
'@
    },
    @{
        title  = 'FR-23 Affiliate disclosure and UK ad-standards compliance pass'
        labels = 'fr,needs-human'
        body   = @'
**Review:** {0} (P1, gap 9)

This is affiliate marketing, promoted in the UK, with an episode built around
Amazon Associates. UK CAP rules on identifying marketing communications and
the Amazon Associates operating agreement both impose obligations, including
constraints on how the programme may be described.

Nothing in the repo mentions disclosure, and `AGENTS.md` currently lets an
agent publish without a compliance gate.

### Deliverable

- `docs/compliance.md`: required disclosure wording for our own posts, what
  may and may not be said about Amazon Associates by name, and the rule for
  hosts who will repost our material.
- A `disclosure:` field in `episodes/_template.yaml`, required non-empty for
  any episode whose CTA is commercial.
- A compliance line added to the `AGENTS.md` "must ask a human" list.
- Specific review of episode 02 ("Amazon Associates at 11:47pm") before it
  is written, not after.

### Needs human

Simon to confirm whether this gets a legal read before episode 02 ships.
'@
    },
    @{
        title  = 'FR-24 Episode 04 title drift pre-empts the Easyfundraising decision'
        labels = 'fr,needs-human,episode'
        body   = @'
**Review:** {0} (P1, gap 10)

Brief rule 8: *do not name Easyfundraising unless issue #13 says so.* Issue #13
is still open.

`metrics.md` already lists episode 04 as **"Easy versus on-our-site"** - a pun
on that name - while `docs/BRIEF.md` calls it "On-site vs off-site portal" and
FR-05 calls it "on-site catalogue vs off-site portal".

Two problems in one line: the title drifts across three files, and the
published version leans on a comparison a human has not signed off.

### Deliverable

- Resolve #13 first: named comparison, or generic "off-site portal" only.
- Pick one canonical title and make `BRIEF.md`, `metrics.md`, and FR-05 agree.
- Add a check to FR-26's CI validator so episode titles cannot drift again.

### Needs human

The naming decision is #13 and belongs to Simon.
'@
    },
    @{
        title  = 'FR-25 TTS comedy-timing quality gate and human VO fallback'
        labels = 'fr,pipeline'
        body   = @'
**Review:** {0} (P1, gap 11)

The register is deadpan British sitcom. Deadpan is entirely timing, and timing
is the hardest thing for TTS to land. The pipeline commits to `open-tts` with
no quality bar, no listen-back gate, and no fallback if the read comes out
flat.

A flat read does not produce a weaker joke. It produces no joke.

Depends on FR-07 (open-tts render path).

### Deliverable

- A listen-back gate before stills: does the button land? Is the pause before
  the turn long enough? Would a stranger laugh?
- Pause and emphasis markers in the YAML `lines` so timing is authored rather
  than hoped for.
- A named fallback: human VO for at least the protagonist if the synthetic
  read fails the gate twice.
- A decision rule - if episodes 01 and 02 both fail the gate, the format
  changes before episode 03, not at week 8.

### Done when

Episode 01 passes a written gate, or the fallback is triggered on purpose.
'@
    },
    @{
        title  = 'FR-26 CI validator for episode YAML and publish safety'
        labels = 'fr,pipeline'
        body   = @'
**Review:** {0} (P1, gap 12)

There is no CI. Every rule the repo already wrote is a comment, not a check.

`_template.yaml` says `named_objects` must be exactly three. `banned` lists
four phrases. `approved` must be flipped by a human. `AGENTS.md` forbids
claims outside the brief. Nothing enforces any of it, and the approval gate is
the only thing standing between an agent and an unreviewed public post.

### Deliverable

A GitHub Action on PR and push that fails when:

- An episode YAML does not match the template schema.
- `named_objects` is not exactly 3.
- Any `banned` phrase appears in `lines` or `companion`.
- `length_target_s` is outside 45-75.
- `cta` is not one of the four allowed values, or `cta_url` does not match it.
- A commercial episode has an empty `disclosure` (FR-23).
- Episode title disagrees with `BRIEF.md` or `metrics.md` (FR-24).
- Any string looks like a secret - `XAI_API_KEY`, `password=`, long tokens.

Plus a separate publish-time guard: refuse to schedule any episode whose
`approved` is not `true`.

### Done when

CI is green on `_template.yaml` and fails a deliberately broken fixture.
'@
    },
    @{
        title  = 'FR-27 Proof pipeline beyond Mereside'
        labels = 'fr,needs-human'
        body   = @'
**Review:** {0} (P2, gap 13)

Mereside Model Flying Club is the only real club the agent may name, and it is
spent in week 7. The strongest asset a host-recruitment campaign can have is
another host saying it worked, and there is no pipeline for generating or
clearing more.

### Deliverable

- A consent-and-clearance template so a club or host can approve being named,
  including what specifically may be quoted.
- A target of 2-3 additional nameable references before week 5, so weeks 5-8
  have fresh proof.
- One host-voice case study: what they deployed, how long it took, what it
  earns, in their words.
- An anonymised fallback pattern ("a model flying club in the north west") for
  use while clearance is pending.

### Needs human

Every real name is a Simon decision under the current `AGENTS.md`.
'@
    },
    @{
        title  = 'FR-28 Accessibility pack: transcripts, alt text, contrast'
        labels = 'fr,accessibility'
        body   = @'
**Review:** {0} (P2, gap 14)

Captions are required, which is a good start and more than most campaigns do.
But there are no transcripts, no alt text rules for quote cards and carousels,
and no contrast standard - on a campaign whose audience builds websites for a
living and will absolutely notice.

The repo has an `accessibility` label with zero issues on it. This is the
cheapest credibility win available to us.

### Deliverable

- Full transcript per episode, committed next to the YAML and posted as the
  first comment or the LinkedIn document.
- Alt text authored for every still, quote card, and carousel slide - add an
  `alt` field beside `carousel_lines` in the template.
- Caption contrast and minimum size standard in the export pack (FR-08).
- A line in `AGENTS.md`: an episode is not shippable without alt text and a
  transcript.

### Done when

Episode 01 ships with a transcript and alt text on every image.
'@
    },
    @{
        title  = 'FR-29 Campaign-level go/no-go and stopping criteria'
        labels = 'fr,needs-human'
        body   = @'
**Review:** {0} (P2, gap 15)

The only stopping rule in the repo is "change the joke target" at week 3.
There is no cost ceiling, no hours ceiling, no scheduled go/no-go, and no
definition of failure for the eight weeks as a whole.

A campaign that cannot be cancelled gets finished out of momentum regardless of
what the numbers say.

### Deliverable

`docs/go-no-go.md` with:

- A week-4 checkpoint with numeric thresholds, using FR-16's definitions and
  FR-15's attribution - continue, change the format, or stop.
- A time budget in hours per week, and what happens when it is exceeded twice.
- An explicit definition of failure for the full eight weeks.
- The pivot options, written before they are needed and therefore before they
  are emotional: change joke target, change protagonist, change platform,
  change from comedy to straight case studies.

### Needs human

Thresholds and the time budget are Simon's to set.

### Done when

The checkpoint is scheduled and the thresholds are committed before episode 01.
'@
    }
)

$existing = @()
try {
    $json = & $gh issue list --repo $Repo --state all --limit 200 --json title 2>$null
    if ($LASTEXITCODE -eq 0 -and $json) {
        $existing = @($json | ConvertFrom-Json | ForEach-Object { [string]$_.title })
    }
}
catch { }

foreach ($fr in $frs) {
    $title = [string]$fr.title
    if ($existing -contains $title) {
        Write-Host "skip (exists): $title"
        continue
    }
    $body = ([string]$fr.body) -f $reviewUrl
    if ($DryRun) {
        Write-Host "DRYRUN would create: $title  [$($fr.labels)]"
        continue
    }
    $tmp = New-TemporaryFile
    try {
        $utf8 = New-Object System.Text.UTF8Encoding $false
        [IO.File]::WriteAllText($tmp.FullName, $body, $utf8)
        $out = & $gh issue create --repo $Repo --title $title --body-file $tmp.FullName --label $fr.labels 2>&1
        if ($LASTEXITCODE -ne 0) { Write-Warning "failed: $title`n$out" }
        else { Write-Host "created: $title -> $out" }
    }
    finally { Remove-Item $tmp.FullName -Force -ErrorAction SilentlyContinue }
    Start-Sleep -Milliseconds 700
}
