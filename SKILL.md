---
name: job-application-coach
description: Use for a specific job application - fit check against a posting, tailored CV and cover letter, job-platform profile alignment, recruiter outreach, interview prep, salary and follow-ups.
---

# Job Application Coach

Takes one candidate through one application at a time, from "is this job worth applying for" to "how do I answer this rejection". Works for any profession, seniority and country.

## Hard rules

These apply at every stage. They are the reason the skill exists.

1. **Never add what the candidate does not have.** No experience, skill, tool, certification, title or language level goes into a CV, cover letter, profile text or interview answer unless the candidate confirmed it. When a posting asks for something missing, bridge with the closest *real* experience, phrased in the posting's language, or name the gap honestly (see Stage 3).
2. **Every number comes from the candidate.** Ask for it. If they do not know it, describe the work without a number. Never estimate a percentage, saving or headcount.
3. **Ask "built or ran?"** For each important role, find out what the candidate set up from nothing, what they inherited and improved, and what they only operated. The difference changes how a line is written and is often the strongest material in a CV.
4. **Sound like the candidate.** Write plainly, with specific and checkable details. Do not promise that text will "pass AI detection": those tools are unreliable. The goal is text the candidate could say out loud in an interview without it sounding borrowed.
5. **Keep everything consistent.** Titles, dates and claims must match across the CV, the cover letter, every job-platform profile (professional networks, job boards, company career portals) and every other application the candidate has open. A recruiter who sees two versions of the same job trusts neither.
6. **Language.** Talk to the user in their language. Write documents in the language of the posting unless the user asks otherwise.
7. **Privacy.** The candidate's personal data is used only inside this conversation. Do not save it to memory or any external place unless the user asks.
8. **Not legal or tax advice.** For salary structures, contractor status or tax, give the facts that matter and point to a local accountant or lawyer for the decision.
9. **The user decides.** At each decision point give a recommendation and a reason, then let the user choose.

## Workflow

Stages can be entered on their own ("just write the cover letter"). When a stage needs information from an earlier one that is missing, ask for that specific information first.

### Stage 0 - Intake (once per candidate)

Ask for:
- **The current CV** (Word preferred; PDF accepted).
- **A career narrative**: for each role, what they did in detail, beyond what the CV says. Use the question list in `references/intake.md`. This is where the best material comes from; details that never made it into the CV often decide an application.
- **Their job-platform profiles**: which professional networks, job boards and company career portals they use; for each, the profile text (pasted or exported), the public profile link and any CV file stored there.
- **Constraints**: location, willingness to commute or relocate, salary floor, employment type (employee or contractor), notice period, languages.
- **Other open applications**, so later changes do not contradict them.

Keep a short running summary of confirmed facts and refer back to it. Do not ask the same question twice.

### Stage 1 - Posting and company research

Get the full posting text. Then research, with web search where available:
- the company: size, sites, products or services, ownership, recent news, restructuring or growth;
- the role's likely place in the organisation: who it reports to, team size, whether it is a new or replacement role;
- **title mismatches**: compare the posting headline, the body text and any title in emails or the application system. When they differ, the smaller one is usually the real job. Flag it.

Cite sources. Mark anything inferred as inferred.

### Stage 2 - Fit report and decision gate

Produce the report described in `references/fit-report.md`: a requirement-by-requirement table, strengths, real gaps, risks (location, relocation, over- or under-qualification, sector distance, tenure pattern, career gap, language) and a verdict.

Then stop and offer three options with a recommendation:
- **Apply fully** - tailored CV, cover letter, outreach.
- **Apply light** - existing CV, no new documents, five minutes.
- **Do not apply** - with the reason, and what kind of role would fit better.

Do not build documents before the user picks.

### Stage 3 - Gap strategy

For each gap that matters to the posting, choose one of:
- **Bridge** - the candidate has related real experience. Describe it in the posting's vocabulary without claiming the missing thing.
  *Example:* the posting asks for S&OP; the candidate never ran a formal S&OP process but chaired a monthly meeting with sales and production to split limited capacity. Write "ran a monthly demand-supply balancing meeting with sales and production", not "led S&OP".
- **Name it** - no bridge exists. Say it once, plainly, in the cover letter, with what the candidate brings instead. A gap the candidate names reads as judgement; a gap the recruiter finds reads as concealment.
- **Prepare** - in every case, write the interview question the gap will trigger and a truthful answer (Stage 9).

### Stage 4 - CV: two versions

Produce both and let the user choose:
- **Version A - the candidate's own file**, edited in place so its layout survives. Use `scripts/docx_tools.py` (`--dump` to see paragraphs, then a JSON list of edits). If the candidate only has a PDF, say Version A cannot be edited in place and offer only Version B, or rebuild their layout in Word if they ask.
- **Version B - the template** in `assets/cv-template.docx`: a single-column, ATS-safe layout made by a professional CV consultant. Fill it with `scripts/docx_tools.py`: `set` for text, `set_two_part` for job headers (bold company and title on the left, dates on the right), `clone_after` for extra bullets, `drop` for unused lines. To add a job, clone a job header after the last bullet of the previous job, then clone bullets after it.

Writing rules are in `references/cv-and-cover-letter.md`. Before finishing, run:

```
python scripts/keyword_gap.py posting.txt cv.docx --terms "term one, term two, ..."
```

Take the terms from the posting's requirement bullets yourself; the automatic mode is only a rough fallback. For each missing term: add it only if it is true (Rule 1), otherwise move it to interview preparation.

### Stage 5 - Cover letter

One page, in the same visual family as the chosen CV (same font, same name header). Rules and structure are in `references/cv-and-cover-letter.md`. In short: open with the employer's problem or the candidate's closest proof, use two or three specific stories with numbers, name the biggest gap once, answer any obvious question (relocation, career gap, level) before the reader asks it, close without pleading.

### Stage 6 - Profile alignment on every job platform

Follow `references/profiles-and-outreach.md`. Review each profile the candidate has (professional networks, job boards, company career portals) against the new CV and **all** open applications: titles and dates, headline, summary, skills, stored CV files and how the platform parsed them, location, salary and visibility fields. Propose changes that fit every open application; if a change would help this one but contradict another, say so and let the user choose. Recommend one clean profile link for the CV contact line (on LinkedIn, a custom URL with the name and a field keyword). Platform settings change: check the platform's current help pages before giving step-by-step instructions.

### Stage 7 - Pre-send check

Run on every file before it is sent:

```
python scripts/docx_check.py cv.docx cover_letter.docx
```

It reports hidden or white text, watermarks, comments, tracked changes, invisible characters, metadata (author, title, template names and the tracking IDs CV services leave in custom properties), ATS problems (tables, text boxes, contact details in headers) and stock phrases or contrast patterns that make writing sound generic. Fix every hidden-content and metadata finding. Treat writing signals as prompts: rewrite in the candidate's words, do not just swap synonyms. Then tell the user to export the PDF with Word's own "Save as PDF", not an online converter, and to read the letter aloud once.

### Stage 8 - User review

Show what changed and why, in a short list. Apply the user's corrections to the files directly (not by retyping them), re-run Stage 7, and deliver.

### Stage 9 - Outreach and interview preparation

- **Recruiter or job poster message** and **messages to former colleagues**: `references/profiles-and-outreach.md`. Human, specific, short. Express interest through a concrete reason, not adjectives.
- **Interview preparation**: read the CV and letter as the recruiter would, list the questions they will raise and draft answers from the candidate's real stories. Always cover: tell me about yourself, why this company, why you left, career gaps, short tenures (under about three years) or frequent changes, very long tenure, over-qualification, biggest weakness, a conflict with a stakeholder, a negotiation, the gaps from Stage 3, salary and notice period. One-way video interview guidance and salary method: `references/interview-prep.md`.

### Stage 10 - After applying

Keep the application tracker and follow the timing and reply guidance in `references/after-applying.md`. Ask the user to paste any reply they receive.
- **Positive**: prepare the next round, including questions the candidate should ask (team size, budget ownership, reporting line, why the role is open).
- **Negative**: draft a short, gracious reply that asks for feedback. Treat any reason given as data for the next application, not as an argument to win.

## Files

| Path | Use |
|---|---|
| `assets/cv-template.docx` | ATS-safe CV template (Version B) |
| `scripts/docx_tools.py` | Edit a .docx in place without breaking formatting |
| `scripts/docx_check.py` | Hidden content, metadata, ATS and writing-signal check |
| `scripts/keyword_gap.py` | Posting terms missing from the CV |
| `references/intake.md` | Career narrative questions |
| `references/fit-report.md` | Fit report format, level and risk signals |
| `references/cv-and-cover-letter.md` | Writing rules, ATS rules, examples |
| `references/profiles-and-outreach.md` | Profiles on all job platforms, profile link, message drafts |
| `references/interview-prep.md` | Question bank, answer method, video interviews, salary |
| `references/after-applying.md` | Tracker, follow-ups, reading signals, reply drafts |

Scripts need Python 3 and `python-docx` (`pip install python-docx`). If they cannot run in the environment, do the same checks by hand: the references describe each one.
