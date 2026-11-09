# Job Application Coach

A Claude skill that takes a candidate through a single job application, end to end:

1. Intake of the CV and a detailed career narrative
2. Company and role research
3. Fit report with an apply / apply light / do not apply decision
4. Gap strategy that never invents experience
5. Two tailored CVs: the candidate's own file edited in place, and a professional ATS-safe template
6. A one-page cover letter in the candidate's voice
7. Profile alignment on every job platform (professional networks, job boards, company career portals), consistent with all open applications
8. Pre-send check for hidden text, watermarks, metadata, tracking IDs and generic phrasing
9. Recruiter and network outreach messages
10. Interview preparation, one-way video interviews and salary method
11. Follow-up timing, reading signals and rejection replies

## Principles

- Nothing goes into a CV, letter or answer that the candidate does not have.
- Every number comes from the candidate.
- Text should sound like the candidate and be specific enough to defend in an interview.
- Titles and dates stay consistent across the CV, every job-platform profile and every open application.

## Contents

```
job-application-coach/
  SKILL.md                     workflow and rules
  assets/cv-template.docx      ATS-safe CV template
  scripts/docx_tools.py        edit a .docx in place without breaking formatting
  scripts/docx_check.py        hidden content, metadata, ATS and writing-signal check
  scripts/keyword_gap.py       posting terms missing from the CV
  references/                  intake questions, fit report, writing rules,
                               job-platform profiles and outreach, interview prep, after applying
```

## Install

### Claude app (web and desktop)

1. Download **`job-application-coach.zip` from the [Releases](../../releases) page** of this repository.
   Do not use GitHub's green "Code > Download ZIP" button: it wraps the files in an extra folder
   (`repo-name-main/...`) and Claude will reject the upload because the folder name no longer
   matches the skill name.
2. In Claude, open **Settings > Capabilities** and turn on **Code execution and file creation**
   (shown as "Create and edit files" in newer layouts). The skill needs it to edit Word files and run its checks.
3. Go to **Customize > Skills**, click **+**, then **+ Create skill**, then **Upload a skill**.
4. Select the ZIP. The skill appears in your list; make sure its toggle is on.

On Team and Enterprise plans, an organisation owner must allow user-created skills and code execution.
Official guide: [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### Claude Code

Copy the `job-application-coach` folder (the one that contains `SKILL.md`) to:

- `~/.claude/skills/job-application-coach/` to use it in all your projects, or
- `.claude/skills/job-application-coach/` inside a repository to share it with everyone working there.

Official guide: [Skills in Claude Code](https://code.claude.com/docs/en/skills).

### Using it

No special command is needed. Claude loads the skill whenever a request is about a job application,
in any language. Attach your CV and paste the job posting, then ask in your own words, for example:

- "I want to apply for this job. Is it a good fit for me?"
- "Tailor my CV and write a cover letter for this posting."

It also works for single steps:

- "Check my cover letter before I send it."
- "Prepare me for the interview at this company."
- "How should I reply to this rejection?"

If Claude does not pick it up, name it directly: "Use the job-application-coach skill."
In Claude Code you can also type `/job-application-coach`.

### Requirements for the scripts

Python 3 and `python-docx`. Claude's code execution environment usually has it; locally:

```
pip install python-docx
```

## For the repository owner: publishing a release

Upload `job-application-coach.zip` as a release asset (Releases > Draft a new release > attach the file).
The ZIP must contain a single top-level folder named `job-application-coach` with `SKILL.md` directly inside it.
To rebuild it from the repository:

```
zip -r job-application-coach.zip job-application-coach -x "*/__pycache__/*"
```

## Quick script examples

```
python scripts/docx_tools.py my_cv.docx --dump
python scripts/docx_tools.py my_cv.docx tailored.docx edits.json
python scripts/keyword_gap.py posting.txt tailored.docx --terms "term one, term two"
python scripts/docx_check.py tailored.docx cover_letter.docx
```

## Privacy

The skill works with personal data. It instructs Claude to use that data only inside the conversation and not to store it anywhere unless the user asks.

## Disclaimer

Salary, contract and tax guidance is general information, not legal or tax advice.

## License

Copyright (c) 2026 Serdar Sevindi.
Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/). See [LICENSE](LICENSE).

- **Free for personal use**: use it for your own job search, adapt it, share it with friends.
- **Not for commercial use**: do not sell it, put it in a paid product, or use it to deliver paid services such as paid career coaching.
- **Credit and share alike**: if you share it or a modified version, credit Serdar Sevindi, link to this repository and the license, and release your version under the same license.

If you would like to use it in a way the license does not allow, ask first.
