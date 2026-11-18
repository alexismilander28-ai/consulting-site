# Site rewrite report, 2026-11-15 (TEST site only)

Branch `ai-team`, commit 1c896ce, deployed to the TEST service only (srv-dbsuvarbc2fs73cl5nkg,
deploy dep-dbt8a4ei0phs73evts60, status `live`). Test URL: https://consulting-site-next.onrender.com.
`main` and the live service (srv-dbrqjnjrjlhs73c8bco0) were not touched. Its autoDeploy was read back as `no`.
`render.yaml` and its CSP are unchanged. No secrets were written to any file.

## What changed

| | Before | After |
|---|---|---|
| Brand | "Carlos Milander" in header, titles and footer | "CMRI Consulting" in header, titles and footer; footer says "Carlos Milander, sole proprietor". About and the photo keep his name |
| Email | alexis.milander28@gmail.com plus the "Alexis is my middle name" note | carlos@cmriconsulting.com; the note is gone |
| Demo wording | "Tested on made-up data" (9 times on AI workers), "made-up" on every sample | "A working demo built around a sample shop; I run it live on a call", once per page. Each card says "Working demo. Sample shop." Numbers say "Sample numbers, not results." |
| Texts | Lead demo was an automated missed-call TEXT; reminders and invoices shown as automated texts; the sample report recommended texting back | SMS demo removed. AI workers page and rules say "Every worker sends email only. None sends text messages." Reminder and invoice samples are emails. The report recommends an email or a call back from a person |
| Access | "The Map needs no access to your accounts", "I don't need your passwords" | "Only with your written authorization, read-only to start", "you sign a one-page access form first", "I change nothing" |
| Prices | No figures, but "price" appeared 18 times ("you get the price in writing") | No figures and no "price"/"precio": "cost", "one fixed fee" |
| AI Supervisor | absent | Home, AI workers (with the duty list), About, leave-behind: "Your AI Supervisor runs the AI. The AI runs the routine. You pick one person. I train them." |
| "Separate company" | "starts after a separate company ... exist" | "starts with a written agreement. They run in your own accounts" (no LLC wording) |
| New pages (EN + ES) | none | **See it work** (`see-it-work.html` / `vealo-funcionar.html`): the booking demo in 6 steps (request, Approve/Decline, calendar, confirmation email, reminder email, Monday numbers), every card labelled Sample, plus "Ask for the live demo". **Receptionist** (`receptionist.html` / `recepcionista.html`): the fixed-answer website chat sample; "The phone receptionist is not offered yet. Nothing on this site answers a phone call." **Privacy** (`privacy.html` / `privacidad.html`): from legal/agreements-2026-11-15/09-privacy-policy.md, without the mailing-address placeholder |
| Nav | The Map, AI workers, About, Español | The Map, AI workers, See it work, About, Español. Footer: The receptionist, Privacy, One-page summary |
| Dark mode | light only | follows the device. The page goes dark, the paper samples stay paper |
| "Text" buttons | "Text me" | "Message me"; the note under it says it opens the visitor's own messages app and Carlos answers it himself |

The facts on See it work come from `ai-consulting/product/build-booking.mjs`, `build-reminders.mjs` and `build-crm.mjs`: the owner approves in Telegram, the calendar is re-checked, the demo calendar entry is prefixed `[DEMO]`, the demo confirmation goes to the owner's inbox only, reminders are email only, STOP/PARAR opt out, and the weekly numbers go to the owner only. The receptionist page follows `product/README.md` (fixed answers, no language model, never states a cost).

## Verify (real output)

**Build:** `python build/build.py` wrote 16 pages (8 EN + 8 ES), 25 to 72 KB each.

**Compliance** (`python build/proof/comply.py site`, rules extended for this rewrite): `16 pages checked / COMPLIANCE OK`.
The same rules run on the old build return 57 made-up, 18 price-word, 14 old-email, 11 SMS-promise and 2 no-access hits, so they do fire.

**Required grep counts** (raw built HTML, base64 images removed):

| Term | Before (10 pages) | After (16 pages) | Deployed test site (16 pages) |
|---|---|---|---|
| price sign ($ € £ + digit) | 0 | 0 | 0 |
| word price / precio | 18 | 0 | 0 |
| guarantee / garantía | 0 | 0 | 0 |
| attorney | 0 | 0 | 0 |
| LLC | 0 | 0 | 0 |
| PO box | 0 | 0 | 0 |
| "no access" | 2 | 0 | 0 |
| "made-up" / inventado | 57 | 0 | 0 |
| alexis.milander28 | 14 | 0 | 0 |
| SMS promise (visible text) | 11 | 0 | 0 |

Info only: 8 `sms:` links remain. Each opens the visitor's own messages app with a note to Carlos (contact, not a workflow). Also 0 hits for: real intelligence, middle name, tested on, separate company, testimonial.

**Screenshot matrix** (`build/proof/prove.py`, served locally with the exact CSP from render.yaml): 16 pages x 375/768/1280 x light/dark = 96 renders, plus a keyboard walk at 1280 and print checks. Result: `GATE OK`. No console or CSP errors, no horizontal overflow, one h1 per page, header links on screen, the phone button opens a text and the desktop button an email, a focus ring on every stop, and the leave-behind prints on 1 page in each language. On the first pass the matrix showed two defects, both fixed before the commit: in dark mode the values in the sample cards were faint, and the 5-link header wrapped at 768.

**axe** (frontend-ui `eyes.py`, all 16 pages, light and dark): 0 violation types on all 32 runs. Each run logs 1 console error: axe fetching the font stylesheet, which the strict CSP blocks. This is a known pitfall in the skill. The matrix, which runs without axe, has 0 console errors.

**Registry verify:** `node os.mjs health consulting-site-deploy` gives `GREEN·parse`.

**Deployed:** all 7 new URLs return 200. The 16 deployed pages are byte-identical to the committed `site/` (`diff -rq` clean). In Chromium, the deployed home page and See it work load with 0 console errors, and their h1s are the new text.

## Left for Carlos / not done

- **Spanish:** 314 new or changed Spanish lines are listed in `research/SPANISH-REVIEW-SITE-2026-11-15.md` for your approval.
- **The test service sends no security headers** (no CSP, no X-Frame-Options). The live service does. This is a setting on the test service, not this commit. The pages were checked under the real CSP locally. Adding the headers to the test service is your call.
- **"The Map is the first thing I offer"** still invites paid work. Your rule is no paid client work before EIN, bank and insurance. Decide the wording before launch.
- **Privacy page** carries no mailing address (none chosen yet) and says "Last updated November 15, 2026". Set the real date at launch.
- The registry verify regex `\[[A-Z ]{3,}\]` would flag the `[DEMO]` sample label if it ever reached index.html. It is only on See it work today.
- Not verified: real phones, screen readers, a stranger's read, the live demo end to end on the hosted n8n this session.
- Nothing goes to the live site until you approve. At launch: merge ai-team to main, then deploy the live service.
