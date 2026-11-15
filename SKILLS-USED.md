# Skills used for the tabbed redesign (branch `ai-team`)

Draft for the owner's approval. Nothing here was installed, pushed or deployed.

## Skills used

| Skill | What it did here |
|---|---|
| `frontend-ui` | The LOOK, JUDGE, PLAN, BUILD, PROVE loop, the "paper and ink" brand limits for this site (terrain section 4), and `eyes.py` for axe and the DOM census. |
| `gate-the-artifact` | Checks ran on the rendered page (visible text per tab, per language), not on the source strings. |
| `verify-decides-done` | The screenshot matrix exits 0 or the work is not done; it was re-run after every change. |
| `derive-dont-recall` | State of the interrupted run was read from `git diff`, a rebuild and a fresh matrix, not from the old screenshots. |
| `humanizer` | New copy checked for staged contrasts, dashes and sales language; two result-sounding headings reworded. |

Listed in the brief but not loaded: `avoid-ai-writing` (overlaps `humanizer`; the new strings are short labels),
`dataviz` (the two charts are plain labelled bars in the existing tokens), `anthropic-skills:built-in-browser`
(Playwright did the rendering, so the browser pane was not needed).

## Skills recommended (not installed)

Found in the plugin directory search. All are optional; none is needed to ship this draft.

| Plugin | Why it could help |
|---|---|
| `frontend-design` (Anthropic) | Official design skill; a second opinion on type, colour and layout for future pages. |
| `Design` (Anthropic) | Has `accessibility-review`, `design-critique` and `ux-copy`; useful before the site goes live. Brings connectors this site does not need. |
| `audit-suite` (community) | Ten audit lenses, including accessibility and performance, plus web animation guidance. |
| `VectorLab UI/UX Skills` (community) | Small focused skills for typography, spacing, keyboard, reduced motion and viewports. |
| `Fairmind Design` (community) | WCAG 2.1 AA audit agents (contrast, keyboard, screen reader). Figma parts do not apply here. |
| `UI Design Review` (community) | Reviews the rendered page on phone and desktop the way a designer would. |

No matching skills were found in the account's own skill library.

## New skill saved from this job

`~/.claude/skills/website-redesign/` holds the workflow and the helper scripts (CSP server, screenshot matrix,
i18n coverage check, contact-sheet builder).
