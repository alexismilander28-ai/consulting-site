# Attention plan: from "looks AI-made" to "I should text this guy"

Written 2026-11-15. PLAN ONLY, for the owner to approve. Nothing on the site was changed, pushed,
installed or sent. Scope is the draft on branch `ai-team` (test copy: consulting-site-next). The
live public page is not touched by any step here.

Goal: a shop owner in the Wilkes-Barre, Scranton, Hazleton or Allentown area lands on the page,
understands in five seconds who this is and what he offers, and takes one step: asks for the free
missed-call test, or calls or texts (570) 392-9271.

Rules every step obeys: no prices. No guarantees or promised jobs, savings or results. No fake
testimonials, logos, ratings or stock people. AI always disclosed as automated. Every sample
labeled as made-up. Name is "Carlos Milander" only. No cookies, no analytics.

---

## 1. The diagnosis, in five lines

1. The first thing the eye lands on is a drawn map illustration, not a person. Nobody is there.
2. The home page is a menu of six identical icon cards. It asks the visitor to choose before it has given a reason to care.
3. Nine tabs plus two toggles make it look like an app. On a phone the tab row runs off the edge.
4. The honest strengths (he works alone, he comes in person, Wilkes-Barre area, Spanish) are buried in the About tab. The phone number is not in the first phone screen.
5. The headline talks about the visitor's failure ("the jobs you lose") in a light-then-bold type trick, then says the AI workers "fix it", which reads as a result claim. It does not say what Carlos does on a Tuesday.

Tells check, read from the two home screenshots only (not a full measured run): 8 of the 24
checks fail on the home screen alone (A1 photo, A2 illustration leads, A4 phone as text on a
phone, A5 headline tail, A7 nav, B1 card wall, B7 icon tiles, D1 check-mark row of three). Six
fails is the line where a stranger says "AI made this". The rest are NOT MEASURED yet.

---

## 2. Art-direction brief (one page)

**Who is speaking.** Carlos Milander, one person. He travels to shops and offices around
Wilkes-Barre, Scranton, Hazleton and the Allentown area. He talks to owners of trade and service
businesses (HVAC, plumbing, auto, a dental front desk) with roughly 5 to 30 people. English, and
Spanish in usted written as its own text.

**The one message (no promise in it).** "I'm Carlos. I come to your shop myself, look at what
happens to your calls and quotes, and hand you a written report. You can start with a free test
of how your business answers a new customer."

**Offered today / not yet.** Today: the free missed-call test, and the Map (a paid visit and
written report; the price is given in writing before he commits, never on the site). Not yet:
building and running AI workers. The page says so in one plain status line.

**Tone.** A neighbor who is good with this stuff, across a counter. Short sentences. Says what
he does not do. Never excited.

**Material world.** A printed report, a clipboard, a pen, a phone, a work order, a kitchen or
shop table, his car. Every picture and texture comes from this list. Banned: robots, brains,
circuits, glowing nodes, abstract blobs, drawn maps as decoration.

**The one bold move.** A large real photo of Carlos holding the printed sample report, at the
top of the page, with the headline beside it (under it on a phone). Everything else stays quiet.
Second-best if no photo arrives in time: the headline set very large on plain paper, nothing else.

**Three things removed.** The six-card menu. The drawn path illustration. The nine-tab bar with
the theme switch.

**Palette (4 values, to be measured on the render).**
- Ground: plain uncoated paper, about `#F6F3EC`. Not yellow cream.
- Ink: warm near-black, about `#1C1A17`.
- Accent: ballpoint blue, about `#1D3F9C`. One job only: things you can press.
- Signal: red pencil, about `#B4281E`. Only for the marks on the sample report.
Blue is kept on purpose: cream with terracotta is itself a known AI-page look.

**Type.** Source Serif 4 (already on the site) for headline and body, one weight, no bold tail.
The page should read like a letter that comes with a report. Source Sans 3 only for buttons,
the header and form labels. Body 19 px desktop, 17 px phone. Headline about 52 px desktop, 32 px
phone. No ALL-CAPS labels. No handwriting font: handwriting is a scan of his real hand or absent.

**Shape.** Two corner radii (buttons, photos), paper artifacts square. Two shadows at most.
One artifact tilted 2 degrees. Almost no motion.

**Three adjectives.** Local. Plain. In person.

**Must never look like.** A software startup landing page. An "AI agency" page (dark, glowing,
purple or cyan). A franchise template with stock smiles and star badges.

**Host limits (read from `render.yaml`).** The served policy is
`default-src 'none'; img-src data:; font-src https://fonts.gstatic.com; form-action mailto:` and
no `media-src`. That means: photos only work pasted inside the file (heavy), audio and video
cannot play at all, fonts must come from Google. Changing this is an owner decision (section 8).

---

## 3. New page architecture

Built phone first. Four small pages instead of nine tabs in one 294 KB file.

**Header (every page):** `Carlos Milander` on the left. On the right, as plain text links:
`(570) 392-9271` and `Español`. Below or beside: The Map, AI workers, About. That is the whole
navigation: **The Map · AI workers · About · Español.** No theme switch (the page follows the
device setting quietly or is light only). Nothing scrolls sideways.

**First screen on a phone (375 x 812), top to bottom:**
1. Name and phone number.
2. Photo: Carlos with the printed report. Caption: "Carlos Milander, Wilkes-Barre area."
3. Headline (one of section 6).
4. One sentence: "I work alone and I come to your shop myself. English or Spanish."
5. One filled button: **Get the free missed-call test.**
6. Plain text under it: "or call or text (570) 392-9271".

On desktop the same six things sit in two unequal columns (photo about 5, text about 7).

**The short scroll (four bands, no two alike):**
1. *How the free test goes.* Narrow column, four numbered sentences already written in the draft (you send your number, he sends one ordinary request under his real name, he notes the times, you get them privately; one test, no sales call unless asked).
2. *The sample Map.* Wide: two or three photographed report pages running off the right edge. Label beside it: "Sample report for a made-up HVAC shop. Not results." Link: "See the sample report".
3. *What an automated text looks like.* A phone in a hand showing the text thread, first line says it is automated. Label: "Demo on a test number. Not offered to customers yet."
4. *Who and where.* Three short paragraphs in first person, the towns by name, how a visit goes, then the phone number large, the button again, and the email.

Footer: name, area, "No cookies. No analytics."

**Height budget:** home at most 3,200 px tall at 375 wide and 2,400 px at 1280 wide. One filled
button per screen.

**What moves out of the home page:**
- "The leaks" and "A made-up week" go to The Map page.
- "Samples" splits: report pages to The Map, text demos to AI workers.
- "Services" and "Questions" shrink to five questions at the bottom of About (including how the price is given and who owns the accounts).
- "AI team" becomes AI workers, opens with the status line "built and tested on made-up data; none runs for a customer yet".
- Gone: card menu, hero drawing, check-mark row, pager arrows, theme switch.

**Spanish as its own page.** `/es/` with its own address, written from the facts, not swapped
in by a script. A Spanish speaker can be sent a link that opens in Spanish, and the header shows
`English` instead. Every caption, label and transcript exists in both. Carlos reads all of it
before it goes anywhere.

---

## 4. The attention engine, without fake proof

Ranked by how hard each pulls on this audience:

1. **The free missed-call test (the main door).** It is about *their* business, costs nothing, and the result is their own measured time, so no claim is needed. It is the only filled button on the page. On a phone it should open a ready-written text message to (570) 392-9271; email stays as the second way.
2. **"I come to your shop myself", with his face and the towns.** The competitors hide behind logos. One person with a name, a town and a phone number is the thing they cannot copy.
3. **The real sample Map, as paper.** Printed, on a table, photographed. Shows exactly what the paid visit leaves behind. Labeled made-up.
4. **A captioned demo of the automated text.** Phone screenshots (or a silent screen recording) of the test system, first line "This is an automated message". No voice is used anywhere, which also keeps his voice rule safe.
5. **Spanish as a real page.** For a Spanish-speaking owner, "Atiendo en español" from a native speaker in the first screen is the hook.
6. **The honest status line.** "Offered today: the Map. Not yet: the AI workers." Disclosure is the trust a new business really has.
7. **His own question from the follow-up script,** as a line lower on the page: "Of every 10 quotes you send, how many get a second call from your office?"

**Off-site pieces that would feed the site (options only, nothing started):**
- *One-page leave-behind*, English one side, Spanish the other, same photo and headline, a QR code to the test. Needs no account. Good for walk-ins and BNI.
- *Google Business Profile* as a service-area business (home address hidden), name "Carlos Milander". Owner creates and verifies it himself. No reviews are asked for until real customers exist.
- *Chamber or BNI listing* in the area he chooses, and the 20-minute Spanish talk already in the sales plan.
- *Other directories* (Bing, Apple Maps) later, same name and number everywhere.
Note: public listings make the business visible to anyone who searches his name. His call.

---

## 5. Imagery plan for a business with no clients

**Exactly these pictures:**

| # | Picture | Where it goes | Who takes it | Label |
|---|---------|---------------|--------------|-------|
| 1 | Carlos at a table or desk by a window, holding or reading the printed sample report. Landscape and portrait. | Home, first screen | Family member or a phone on a timer | Caption with his name and area |
| 2 | The printed sample report on a table with a pen, from above and at an angle, two or three pages fanned. | Home band 2, The Map page | Carlos | "Sample report for a made-up HVAC shop. Not results." |
| 3 | A phone in his hand showing the demo text thread from the test system. | Home band 3, AI workers | Carlos | "Demo on a test number. This message is automated." |
| 4 | Two street views from towns he serves, from public ground, no business as the subject. | About | Carlos | Town name |
| 5 | One page of his own notebook or visit checklist, flat. | About or The Map | Carlos | none |

**What the owner must supply:**
- The five shots above as original files (not copies sent through a messaging app). About 30 to 45 minutes with a phone in daylight.
- The sample Map printed on plain paper (three pages). The made-up shop name must be visible on it.
- The demo system running on a test number long enough to take the phone shots.
- His read of every Spanish line.

**Rules for the shoot:** his own home, desk, car or a public street. Not inside any real
business, and no shop sign or van in frame, because that would suggest a client. No one else
recognizable. No filters. Location data is stripped before any file is saved to the project.

**Fallbacks, in order:** (a) no new photos yet: a type-only first screen with the existing
headshot small beside his name; (b) no printed report: the report pages rendered as square paper
sheets, labeled; (c) nothing at all: fewer, plainer sections. Never a stock or AI-generated image.

---

## 6. Copy direction

First person. Named towns and trades. What happens on the day. Statements about what Carlos
does, not about what the visitor is losing. Sentence case.

**Five sample headlines (for the owner to pick from or rewrite; Spanish is a draft for his review):**

| # | English | Español |
|---|---------|---------|
| 1 | I'll contact your business the way a new customer would, and tell you how long the answer took. | Me comunico con su negocio como lo haría un cliente nuevo y le digo cuánto tardó la respuesta. |
| 2 | I'm Carlos. I come to your shop and write down where calls and quotes go unanswered. | Soy Carlos. Voy a su negocio y anoto dónde se quedan sin respuesta las llamadas y los presupuestos. |
| 3 | Find out how long a new customer waits to hear back from your office. | Sepa cuánto espera un cliente nuevo para que su oficina le conteste. |
| 4 | One visit to your shop. One written report on your calls and your quotes. | Una visita a su negocio y un informe escrito sobre sus llamadas y sus presupuestos. |
| 5 | Of every 10 quotes you send, how many get a second call? | De cada 10 presupuestos que envía, ¿a cuántos les da una segunda llamada? |

Recommended: number 2 as the headline (it carries the person and the visit), number 1 as the
sentence beside the test button, number 5 lower on the page.

**Words and habits to avoid, both languages:**
- Any figure with a currency sign, "cheap", "best", "free quote". ("Free missed-call test" stays: it is the named door and carries no figure.)
- guarantee, promise, save, more jobs, never miss a call, results, ROI, percentages. In Spanish: garantía, ahorre, más trabajos, resultados.
- "fix", "solve", "recover" said of the AI workers. Say what the worker does: "sends a text that says it is automated".
- "AI team", "AI employees" as if they were people. Use "AI workers" and call them automated.
- solutions, seamless, streamline, transform, unlock, leverage, cutting-edge; soluciones, potencie, transforme, de vanguardia.
- Groups of three, check-mark rows, dashes as sentence glue, "not X but Y", question headings like "Tired of missed calls?".
- "we" and "our team". He works alone.

---

## 7. Build plan: four small milestones

Each one ends with a draft on the test copy only, a short report, and a stop for the owner.
Build time is the assistant's; Carlos's time is listed separately. Total: about 22 to 27 hours
of build, about 3 hours of Carlos.

**M1. New home page in English, type-led (6 to 8 h).**
- Deliverable: the brief saved as `design/ART-DIRECTION.md`; new first screen and four-band scroll; four-link header; paper palette; new copy. Uses the existing headshot only.
- Carlos provides or decides: decisions 1 and 2 in section 8.
- Proven by: before and after screenshots at 1280 and 375; full 24-line tells table with measured counts (target 2 or fewer fails, none above the fold except the photo line, which waits for M2); height budget measured; compliance search for the banned words above plus "BERO", "MCP", "Consulting"; the five-second, squint and swap tests answered from the screenshot.

**M2. Real pictures in (4 to 5 h, plus Carlos 45 min of shooting).**
- Deliverable: pictures 1 to 3 cropped, compressed, location data stripped, placed with their labels.
- Carlos provides or decides: the photos, the printed report, decision 3 (photos) and decision 4 (host policy).
- Proven by: tells line A1 passes at both widths; page weight reported; labels visible beside every sample in the screenshot, not only in hidden text.

**M3. Inner pages and the Spanish site (7 to 9 h, plus Carlos 1 h reading).**
- Deliverable: The Map, AI workers and About pages cut down from the existing tabs; `/es/` versions of all four written as their own text.
- Carlos provides or decides: reads and corrects every Spanish line; decision 7.
- Proven by: screenshot matrix (4 pages x 2 languages x 2 widths); compliance search in both languages; every sample label and "automated" line present in both; nav measured at 375.

**M4. Demo, final critique, owner gate (4 to 5 h).**
- Deliverable: the text demo as labeled still frames with a transcript, or a silent captioned screen recording if decision 5 allows it; side-by-side before and after sheet; final tells table.
- Carlos provides or decides: decisions 5, 6 and 8; optionally shows the phone page to two or three people for five seconds and asks "who is this and what does he do".
- Proven by: transcript beside the demo in both languages; no autoplay; final report listing what was not verified (real phones, a stranger's reaction, the live host). Then it stops. Moving it to the public site is his separate decision.

---

## 8. Decisions needed from the owner

| # | Decision | Recommendation | Blocked until answered |
|---|----------|----------------|------------------------|
| 1 | Approve the direction: his photo and the printed report lead, plain paper look, four links, short home page, no theme switch. | Yes. | Everything. |
| 2 | Pick or rewrite the headline (section 6). | Number 2, with number 1 beside the button. | M1 copy. |
| 3 | Will he do the 45-minute phone shoot and print the sample report? | Yes, at home or in his car, not in any real business. | M2. Without it the page stays type-only. |
| 4 | Allow the test site to load its own files: add `'self'` for images, media and fonts in the host policy. No outside hosts. | Yes, on the test copy first. It also lets fonts stop loading from Google. To confirm in M2: that the change lands only on the test service, since `render.yaml` names the public one. | Good-quality photos, any recording, self-hosted fonts. Without it photos are pasted into the file and kept small. |
| 5 | Demo format: still phone screenshots with transcript, or a silent captioned screen recording. | Stills first (work today). Recording later if decision 4 is yes. No voice either way. | M4 demo. |
| 6 | Main door on a phone: the button opens a ready-written text to (570) 392-9271, with email second. Is he fine getting texts from strangers on that number? | Yes. Texting is what this audience does. He answers by hand. | Button behavior. |
| 7 | The email shown is `alexis.milander28@gmail.com` with a note explaining the middle name. Keep it, or use an address under the name Carlos? | Change it when convenient. He would create it himself. Not a blocker. | Nothing. |
| 8 | Off-site options: leave-behind, Google Business Profile, chamber or BNI listing. | Leave-behind now (no account). Google profile after the site is approved, created by him. | Nothing on the site. |

**Can start the moment 1 and 2 are answered:** M1. **Waits on him:** M2 (photos, policy),
the Spanish sign-off in M3, the demo choice in M4.

**Not verified in this plan:** the tells count beyond the home screenshots; contrast values of the
proposed colors; how the page looks on a real phone; the Spanish headlines (drafts until he reads
them).
