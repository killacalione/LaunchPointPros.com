# Current-site audit — Milestone 0

Inspection date: 2026-09-04. All website defects below are deferred; index.html,
styles.css, and script.js remain byte-for-byte unchanged. Severity indicates
potential impact, not permission to expand this milestone.

## Baseline

- Branch: `feat/site-growth-redesign`, clean and up to date with its origin tracking branch.
- HEAD: `06f2a0d7a0e280ff639b84d7ffa27c74a1e7dd93`.
- Origin (fetch/push): https://github.com/killacalione/LaunchPointPros.com.git
- Upstream (fetch/push): https://github.com/launchpointpros/LaunchPointPros.com.git
- Configured remote roles suggest working repository and production baseline;
  GitHub fork metadata was not independently queried.
- Tracked baseline files: `.gitignore`, `README.md`, `index.html`, `script.js`, `styles.css`.
- All five files use LF in both the index and working tree.
- Local `.DS_Store` exists but is ignored and untracked. Existing ignore rules cover
  dependencies, build output, environment secrets, and logs; `.env.example` is allowed.

Baseline commands: `git status`, `git branch --show-current`, `git remote -v`,
`git log --oneline --decorate -n 10`, `git ls-files`, `git rev-parse HEAD`,
`git ls-files --eol`.

The available history at inspection was:

```text
06f2a0d Ignore macOS .DS_Store files
84e0214 Add files via upload
83412ac Initial commit
```

`main`, `origin/main`, and `upstream/main` pointed to `84e0214`.

## Current structure

One static HTML homepage with a stylesheet and browser script; no package manifest,
build tooling, backend, or framework. Sections cover hero, services, process, about,
and contact, followed by the footer. The HTML includes a header, navigation, main,
footer, one h1, title, description, language, and viewport metadata.

## External dependencies

- Google Fonts: Outfit, weights 300–800, with preconnect and display=swap.
- cdnjs: Three.js r134, GSAP 3.12.2, ScrollTrigger 3.12.2.
- Scripts load sequentially near the end of the body, before the local script.
  No integrity attributes or local fallback are present.
- Local CSS and JS references use the existing `?v=32` query string.

## Existing functionality

Fragment links navigate to four section IDs; no duplicate IDs, broken local
fragment targets, bare-hash placeholders, or javascript-scheme links were found.
GSAP animates the hero, canvas, cursor, and magnetic buttons. Three.js draws an
animated wireframe arrow. Navigation updates an active class on scroll.
The email link uses mailto; mailbox ownership/delivery has not been verified.

## Known defects

- **Critical:** None identified in this inspection; this is not a security certification.
- **High:** `script.js:69–92` simulates contact success, logs the entered email, and
  clears it after three seconds without a network submission. Visitors may believe
  a lead was delivered when none was sent.
- **High:** CSS hides the native cursor globally. Unguarded GSAP/ScrollTrigger setup
  runs before other initializers, so a CDN failure can abort initialization and
  leave the custom cursor unable to follow the pointer. This failure path is a
  source-level finding; CDN blocking was not simulated.
- **Medium:** `index.html:148` contains an extra closing section tag, recovered by
  the browser but reported by the lightweight validator.
- **Low:** GSAP targets absent `.hero-badge`; `.project-card` also appears in JS
  selectors despite no matching HTML. CSS retains work/project, hero-badge, and
  gradient-orb selectors without corresponding markup.
- **Low:** `--transition-fast` is referenced but never defined. Navigation assigns
  `.active` without a matching style; an empty section identifier matches every
  navigation href. Nested section offsets also deserve review before relying on
  this highlight logic.
- **Low:** No favicon is supplied; the local browser requested favicon.ico and received HTTP 404.
- **Low:** The script logs a generic load-success message before DOM initialization
  has demonstrated success.

## Accessibility observations

- **Medium:** The email input has only a placeholder, no associated label or ARIA
  name, and `outline: none` without a replacement focus treatment.
- **Medium:** No prefers-reduced-motion handling exists for CSS animation, GSAP,
  WebGL animation, or smooth scrolling.
- **Medium:** Contact controls are inside a div, not a form. Only click handling is
  implemented; native form submission and email validity checks are not used.
- **Medium:** Global cursor hiding has no coarse-pointer or no-JavaScript fallback.
  Decorative canvas/SVG content lacks explicit assistive-technology treatment.
- Keyboard navigation, contrast ratios, and screen-reader usability have not been
  comprehensively tested; no accessibility compliance claim is made.

## Performance observations

- **Medium:** WebGL renders continuously with requestAnimationFrame, including
  when scrolled away; there is no visibility-based pause. Pixel ratio is capped at 2.
- **Medium:** External scripts must load before initialization; fonts and CDNs add
  network dependencies. Mouse movement starts GSAP tweens; blur effects and a
  large canvas add rendering work. These are risks, not measured timing regressions.
- **Low:** Unused styles add maintenance and transfer overhead. No Lighthouse or
  Core Web Vitals measurement was performed.

## SEO observations

- Existing title: “LaunchPoint - Digital Innovation for Growing Businesses”.
- Existing description: “LaunchPoint helps businesses build better digital
  experiences through modern web design, digital systems, and AI automation.”
- **Medium:** No canonical URL, Open Graph, or social-card metadata is present.
- **Low / future work:** No robots.txt, sitemap, or structured data exists. Their
  absence does not itself establish indexing failure; schema must use verified
  business information and must not invent reviews or ratings.

## Lead-generation observations

- **High:** “Email sent!” is simulated; there is no real backend or booking integration.
  Any non-empty string triggers the success state. Console logging can expose
  entered contact information locally.
- **High:** “50+ Projects Delivered”, “95% Client Satisfaction”, and “5+ Years
  Experience” have no supporting evidence in this repository. They are unverified,
  not established as false. No content was rewritten in this milestone.

## Risks / technical debt

- External-library failure and disabled-JavaScript behavior are fragile.
- **Medium:** Small-screen CSS stacks navigation and hides floating cards, but
  preserves the 300px hero-visual area. The sticky stacked header occupies a large
  portion of a phone viewport. Overflow hiding may conceal layout problems.
- Repository safety validation is heuristic: it scans current tracked and
  non-ignored untracked UTF-8 text, not history, ignored files, or binary contents.
  It recognizes selected credential signatures and common personal local paths,
  not every possible secret or absolute path. Symlinks fail for manual review.
- HTML checks target explicit markup; valid optional end-tag syntax may warn.
  Contact-success detection flags the existing implementation pattern, not arbitrary
  obfuscated or rewritten fake backends. No warning should be read as approval to ship.

## Verification evidence

- Python validator: zero errors, three expected warnings (stray tag, email logging,
  and success-message/backend verification).
- Nine validator tests use disposable Git repositories to exercise clean and
  warnings-only results, missing source, tracked ignored files, excluded ignored
  files, safe templates, credential/path blocking and redaction, and self-matches.
- JavaScript syntax check and diff whitespace check pass.
- Local HTTP server served the homepage, CSS, and JavaScript successfully.
- Browser inspection: actual desktop viewport 1280 × 720; actual mobile viewport
  390 × 844. The hero renders at both sizes, with the intended stacked navigation
  on mobile. Document scroll widths were 1272 and 382 respectively; no document-level
  horizontal overflow was measured at those sizes. This does not rule out clipped elements.
- Desktop browser logs showed two GSAP missing-target warnings (one explicitly
  names `.hero-badge`) and no error-level messages. The wireframe arrow and styled
  hero rendered. No new browser-breaking errors were observed.
- This was a homepage rendering smoke check, not a complete mobile interaction,
  keyboard, assistive-technology, CDN-failure, or performance test.
- GitHub Actions has not run remotely; no commit, push, PR, or deployment was made.

## Deferred items

All listed site defects, claim verification, real lead delivery, accessibility and
performance remediation, metadata, responsive refinements, and unused-code cleanup
remain deferred to approved future work. No source correction was made in M0.
Astro migration (M1) and later milestones have not started.
