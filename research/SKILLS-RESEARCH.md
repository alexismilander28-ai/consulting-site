# Skills research: making the site look hand-made

Written 2026-11-15. Research only. Nothing was installed, nothing on the site was changed.
Third-party skill text was read as data; no instruction inside any of it was followed.
The skill built from this is `~/.claude/skills/site-wow-factor/`.

How each entry was judged: (a) does it demonstrably steer away from the generic AI look,
(b) are its rules specific enough to check, (c) is it safe (scripts, hooks, network, hidden
instructions). "Read" says what was actually read this session.

## Ranked top 8

### 1. Anthropic `frontend-design` (official)
- URL: https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design
  and the background article https://claude.com/resources/articles/improving-frontend-design-through-skills
- Read: the full SKILL.md (about 80 lines) and the article.
- Good: the clearest statement of the cause. The article calls it "distributional convergence":
  with no direction a model picks the most common choice at every step. The skill answers with a
  two-pass plan (plan, then strike whatever is the default for any similar page) and a named list
  of tells: eyebrow labels, one accented word in a headline, identical rounded cards, mono for
  small labels, arrows on every link, cream plus terracotta, near-black plus acid accent.
- Take: ground the look in the subject matter; one bold element; every border, label and divider
  must carry information; line length under 80 characters.
- Risks: none found. Markdown only, no scripts, no network. Our draft breaks two of its tells
  today (accented last words in the headline, identical cards).
- Recommendation: **inspiration only; already absorbed.** `frontend-ui` quotes its ban list. Safe
  to install after the owner approves, but it would add little.

### 2. Impeccable (Paul Bakaus)
- URL: https://github.com/pbakaus/impeccable
- Read: README only (the individual reference files were not read).
- Good: the largest public catalogue of AI design tells, plus a deterministic detector (the README
  says 62 rules) and steering verbs such as `bolder`, `quieter`, `distill`, `typeset`.
- Take: the idea of a deterministic tells check that runs on the render, and the specific tells:
  one font for everything, purple-to-blue gradients, cards inside cards, grey text on colour, a
  rounded icon tile above every heading. Also the habit of writing PRODUCT.md / DESIGN.md first.
- Risks: real ones. Installs hooks that run on file edits; downloads a binary to the home folder
  on first use; fetches "visual directions" from its own site even with telemetry off; telemetry
  is on unless disabled; its live mode can launch a CLI agent with approvals disabled. Apache 2.0.
- Recommendation: **inspiration only. Do not install as shipped.**

### 3. Vercel Web Interface Guidelines
- URL: https://github.com/vercel-labs/web-interface-guidelines
- Read: README.
- Good: the most checkable list in the field. Focus rings, 24/44 px targets, 16 px inputs on
  phones, `transform`/`opacity` only, reduced-motion variants, curly quotes, tabular numerals,
  non-breaking spaces between number and unit, two-layer shadows, concentric radii.
- Take: the typographic finish items (curly quotes, real ellipsis, non-breaking spaces) are
  exactly the small things that separate set type from generated type.
- Risks: its copy rules are Vercel house style, not universal. Whether the packaged
  `web-design-guidelines` skill fetches the rules from GitHub at run time was not confirmed.
- Recommendation: **inspiration only; already in `frontend-ui/references/doctrine.md`.**

### 4. Website Copywriting & Positioning (community plugin, Anthropic directory)
- URL: listed in the claude.ai plugin directory (author Sergey Skripko); no public source read.
- Read: catalogue description only. Five skills: brand-voice, copy-diagnose, copy-edit,
  copy-proof-check, landing-page-copy. Listed as "contained" (no connectors).
- Good: the description matches our rules closely: diagnose before rewriting, keep every number
  and name, check claims against evidence, and it says proof, testimonials and urgency are
  "never invented".
- Take: the order of work (diagnosis, then edit, then a proof check against what is true).
- Risks: community author, text not inspected, so the claims above are the listing's, not verified.
  "Conversion copywriting" tools tend to push urgency and outcome claims.
- Recommendation: **worth a look after the owner approves, and only after its SKILL.md files are
  read.** Until then `humanizer` and `avoid-ai-writing` cover the ground.

### 5. Emil Kowalski `emil-design-eng`
- URL: https://github.com/emilkowalski/skills
- Read: SKILL.md (about 420 lines).
- Good: motion rules with numbers. Press feedback 100-160 ms, most UI under 300 ms, exits faster
  than entrances, never `ease-in`, never from `scale(0)`, no animation on things used many times
  a day, hover effects only behind `(hover: hover) and (pointer: fine)`.
- Take: the "should this animate at all" ladder. A consultant's page needs almost none.
- Risks: no scripts or network. It does contain behaviour instructions (a fixed greeting, a
  required review table) that are about the skill, not design.
- Recommendation: **inspiration only; already in `frontend-ui/references/motion.md`.**

### 6. taste-skill (`design-taste-frontend`)
- URL: https://github.com/Leonxlnx/taste-skill
- Read: README only.
- Good: the only public skill found with honest-imagery rules: library photos may not be presented
  as the client's own and are marked as stand-ins; non-tech pages get photo-led or type-led
  moments and no WebGL; a copy lint that fails placeholder text and invented street numbers.
- Take: those imagery rules, and "left and right content edges must match".
- Risks: Node scripts, a Stop hook as finish gate, network use for photos, fonts and icons,
  an install script that symlinks into agent folders. It also deals fonts and palettes from a
  fixed library, which is a template with more steps. MIT.
- Recommendation: **inspiration only.**

### 7. Anthropic Design plugin (`design-critique`, `ux-copy`, `accessibility-review`)
- URL: https://github.com/anthropics/knowledge-work-plugins/tree/main/design
- Read: `design-critique/SKILL.md`. The other two were not read.
- Good: a simple critique order (first impression, usability, hierarchy, consistency,
  accessibility) that ends in three ranked recommendations and a "what works" section.
- Take: "first impression" as its own step, before any measuring.
- Risks: trusted publisher, no scripts, but the plugin bundles nine remote connectors (Figma,
  Slack, Gmail and others) that this job does not need.
- Recommendation: **skip installing.** The ten-line critique in `frontend-ui` is stricter.

### 8. Axe Accessibility (Deque, partner plugin)
- URL: https://github.com/dequelabs/axe-accessibility
- Read: catalogue description only.
- Good: Deque wrote axe; scan, fix, verify loop including keyboard tests.
- Take: nothing new. `frontend-ui/scripts/eyes.py` already runs axe locally.
- Risks: runs through a remote MCP server, so page content leaves the machine.
- Recommendation: **skip.**

Also looked at and not ranked: UI Design Review by UXKIN (community, remote MCP server),
UI/UX Pro Max (installs through an npm CLI; not read), A11y Enforcer (community, duplicate of
axe). The claude.ai skills search returned nothing for these topics.

**Bottom line:** nothing needs installing. The public skills are strong on type, colour, motion
and tells, and `frontend-ui` already carries that. What none of them cover is what this site
lacks: real imagery for a business with no clients, proof without fake proof, and local,
first-person copy. That is what `site-wow-factor` adds.

## Craft principles digest (one page)

**1. People look at real photos and skip filler.** NN/g eye-tracking: users study photos of real
people and real products and ignore stock models and decoration; on one site team portraits got
more attention than bios that took three times the space.
https://www.nngroup.com/articles/photos-as-web-content/ (2010). The 2019 About-page study found
the same: real staff photos helped, stock hurt, easy contact details helped.
https://www.nngroup.com/articles/about-us-information-on-websites/
*For us:* one honest photo of Carlos in a real place beats 87 tidy SVGs.

**2. Trust comes from four things, none of which need testimonials.** Design quality, up-front
disclosure, complete and current content, and a connection to the rest of the web.
https://www.nngroup.com/articles/trustworthy-design/ (2016). The study adds that service buyers
want to see the process and the person doing the work, that on-site testimonials are viewed
with suspicion anyway, and that typos and vague labels cost trust fast.
*For us:* a name, a face, a phone number, the towns, what happens on a visit, what is and is not
offered yet. Note the tension: that study found people leave when rates are hidden. The owner's
rule is no prices on the site, so say plainly how and when the price is given.

**3. The AI look is the look of no decision.** Anthropic's own account is that models fall to the
most common choice unless something specific pulls them off it.
https://claude.com/resources/articles/improving-frontend-design-through-skills. A design agency
makes the same point about fonts: the tell is that a face "appears unchosen".
https://www.925studios.co/blog/ai-slop-design-tells (opinion, not research).
*For us:* every element needs a reason that comes from this business. If it would fit any
consultant's page, it is a tell.

**4. Symmetry and sameness read as generated; rhythm reads as edited.** Identical card grids,
one radius, even section heights and centred everything are the house style of templates
(Anthropic skill, Impeccable, taste-skill all list them). Hand-made pages vary: a wide photo, then
a narrow column of text, then a full-width artifact.
*For us:* no grid of more than three like cards; unequal columns; no two adjacent sections with
the same layout.

**5. Type does most of the work.** Body 15-25 px, line spacing 120-145 %, 45-90 characters per
line. https://practicaltypography.com/typography-in-ten-minutes.html. Add the finish items from
Vercel's list: curly quotes, real apostrophes, non-breaking space between number and unit,
tabular numerals in tables. One family used well beats two used timidly; do not accent the last
words of a headline in a second weight.

**6. Restrained colour, warm ground.** The human-looking sites in the competitor study (07, 08)
sit on warm off-white with dark text and one accent. Dark navy with a pale-blue button is the AI
consulting default. Use the accent for one job. Check the count on the render.

**7. Show the thing itself.** The competitor pages that convinced did it with the deliverable:
a real product screenshot (07), a playable demo call with its transcript and a note that the
business is made up (05), a single realistic message (10). Artifacts with paper edges, a staple
shadow, a phone status bar and a slight angle look made; perfectly aligned vector mockups look
generated.

**8. Audio and video demos need text beside them.** Captions for video, a transcript for audio,
visible controls, no autoplay. https://www.w3.org/WAI/media/av/ (WCAG 1.2.x; autoplay falls
under 1.4.2, not re-read this session). A transcript is also what makes a demo credible to
someone who will not press play.

**9. Short navigation, visible.** NN/g measured hidden navigation cutting discoverability by more
than 20 % and recommends that four or fewer top-level links be shown as plain links, on phones
too. https://www.nngroup.com/articles/hamburger-menus/
*For us:* four links and the phone number as text. Nothing scrolls sideways.

**10. Copy sounds like one person in one place.** First person, named towns, named trades, what
happens on the day. No lists of three with check icons, no dash-joined slogans, no claims about
results. Spanish written as its own text, in usted. (NN/g About study: plain language over jargon.)

## Not verified

- Stanford Web Credibility guidelines (https://credibility.stanford.edu/guidelines/) could not be
  fetched (certificate error); not used above.
- Star and install counts quoted by aggregator sites for any skill; not repeated here.
- Impeccable's and taste-skill's reference files and scripts were not read line by line; the
  risk notes come from their own READMEs.
- The Website Copywriting plugin and the UXKIN and Deque plugins: catalogue descriptions only.
- Whether Vercel's packaged skill fetches its rules at run time.
- WCAG criterion numbers for media are from memory, not re-read.
