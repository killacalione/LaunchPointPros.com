# Milestone 1 — Astro migration verification

Verified on 2026-09-05. The existing partial migration was completed on
`feat/site-growth-redesign`, retaining M0 commit
`faa4e3161d6f79595375b8a6af36b8a698eefbd3`. No redesign, backend, deployment,
Cloudflare integration, or Milestone 2 work was performed.

## Architecture and changes

- Retained the partial Astro configuration, lockfile, seven components, shared
  layout, and homepage. No replacement scaffolding or dependency upgrade was needed.
- `src/styles/global.css` is byte-for-byte identical to the M0 stylesheet.
- `src/scripts/site.js` is the M0 JavaScript with only three imports prepended:
  Three.js, GSAP, and ScrollTrigger. Existing initialization and interactions remain.
- The existing processed script tag in `BaseLayout.astro` successfully produces
  a local bundled production script. No script-loading adjustment was needed.
- Normalized original and built HTML matched across all 327 markup/text tokens,
  excluding comments, whitespace, script/stylesheet loading, and the approved
  extra closing section tag. This includes metadata, text, links, IDs, classes,
  SVG attributes, canvas placement, contact markup, and footer.
- Updated repository validation, its fixtures, CI, README, and AGENTS for Astro.
  The M0 audit remains unchanged as historical evidence.
- Removed the original root `index.html`, `styles.css`, and `script.js` only after
  installation, check/build, HTTP, browser, visual, and behavior verification.

## Versions and dependencies

| Item | Verified version |
| --- | --- |
| Local Node | 24.14.1 |
| Local npm | 11.11.0 |
| Python | 3.11.9 |
| Astro | 7.3.1 |
| GSAP / ScrollTrigger | 3.12.2 |
| Three.js | 0.134.0 (r134) |
| @astrojs/check | 0.9.10 |
| TypeScript | 6.0.3 |

The manifest requires Node 22.12+ and npm 9.6.5+. CI selects Node 22 and Python
3.11. Local verification used the existing Node 24 installation; Node 22 results
must be distinguished from that local run.

`npm ci` succeeded with a temporary writable npm cache: 273 packages added,
274 audited, zero vulnerabilities reported by npm at installation time. No
global installation, sudo, or lockfile regeneration was used. Astro commands used
process-scoped `ASTRO_TELEMETRY_DISABLED=1` because its default preferences
directory is unavailable in the sandbox.

`npm ls --depth=0` exits successfully and resolves all five pinned direct packages.
It also labels seven WASM/support packages as extraneous after the clean install:
`@emnapi/core`, `@emnapi/runtime`, `@emnapi/wasi-threads`, `@img/sharp-wasm32`,
`@napi-rs/wasm-runtime`, `@tybys/wasm-util`, and `tslib`. This is recorded without
changing dependency metadata or treating the dependency tree as warning-free.

## Validation and production output

- `npm run check`: 12 files checked after legacy removal; zero errors, warnings,
  or hints.
- `npm run build`: successful static generation of one page.
- `python3 scripts/validate.py`: zero errors; two expected warnings in migrated
  source for email console logging and simulated success requiring a real backend.
- `python3 scripts/test_validate.py`: all 14 tests passed, including Astro-only
  fixtures, missing sources/build output, component placeholder links, rendered
  cross-component fragments, and credential/path scanning of ignored build assets.
- `node --check src/scripts/site.js` and `git diff --check`: passed.
- The validator continues checking tracked and non-ignored untracked files,
  including secrets, personal paths, local metadata, and symlinks. Built output
  is also inspected. These heuristic checks are not a security certification.

Built assets inspected and served successfully:

| Output | Bytes |
| --- | ---: |
| `dist/index.html` | 8,358 |
| `dist/_astro/index.CeDgZi3T.css` | 11,364 |
| `dist/_astro/BaseLayout.astro_astro_type_script_index_0_lang.CjjBpTil.js` | 720,128 |

Both generated asset references resolve. No local-path or credential signatures
were detected in source or generated text. The build reports a JavaScript chunk
larger than 500 kB; the warning was retained, with optimization deferred.

Legacy HTTP on port 8011, Astro development on port 4321, and production preview
on port 4322 returned HTTP 200 for the homepage. Production CSS and JavaScript
also returned HTTP 200. Port 8000 was already occupied, so the baseline server
used 8011 without disturbing the existing process.

## Browser and visual verification

The local in-app browser was used for baseline/production comparisons at actual
viewports of **1280 × 720** and **390 × 844**. Development runtime was also
checked at 1280 × 720. Phone dimensions were emulated; no physical touch-device
or cross-browser claim is made.

| Measurement | Baseline | Astro |
| --- | ---: | ---: |
| Desktop document scroll width | 1,272 | 1,272 |
| Desktop document scroll height | 3,501 | 3,501 |
| Mobile document scroll width | 382 | 382 |
| Mobile document scroll height | 5,720 | 5,720 |

Section dimensions and document positions matched. Mobile measurements included
the 231.523px header, 822.156px hero, 1,354.156px services section, 1,376.984px
process section, 782.242px about section, 530.594px contact section, and 622.664px
footer. These are parity measurements, not an assertion that clipping or the
existing responsive layout is ideal.

Viewport screenshots were captured for the hero, services, process, about/stats,
contact, and footer. Typography, spacing, colors, icons, navigation, cards, and
section layout showed no major visual regression. Floating cards remain visible
on desktop and hidden on mobile. The wireframe arrow renders and animates;
animation-phase differences were expected. Full-page capture produced stitching
artifacts, so viewport captures and DOM measurements were used for assessment.

Behavior exercised:

- Navigation links reached all four fragments on both viewport sizes; active
  classes matched the baseline after scrolling settled.
- ScrollTrigger translated the canvas to 150px on desktop services navigation
  and approximately 149.909px at the mobile services position, matching baseline.
- Desktop cursor followed pointer movement, entered/exited its hover class, and
  magnetic buttons displaced on pointer entry and returned after exit.
- Keyboard Enter on the hero process link navigated to the process section.
- Synthetic contact input produced `Email sent!` on desktop and mobile, temporarily
  disabled pointer interaction, and restored the button/input after the existing
  three-second timeout. Existing synthetic-email console logging was observed.
- An isolated local proxy injected temporary counters around fetch, XHR send,
  sendBeacon, and form submission APIs. The production contact interaction left
  the count at zero before click, during simulated success, and after reset.
  The probe was outside the repository and did not alter shipped source.

Console classification across baseline, production, and development:

- New error-level messages: **none observed**.
- New browser warnings: **none observed**.
- Pre-existing warnings: GSAP missing `.hero-badge` and an empty target, twice
  per initialization. They remained warnings and did not stop other initializers.
- Development-only messages: Vite connection debug messages.

Existing unverified statistics, fake lead delivery, accessibility defects,
navigation edge cases, absent favicon, and performance debt remain deferred.
No Lighthouse, screen-reader, physical-device, CDN-failure, or comprehensive
accessibility audit was performed.

## Final source tree and handoff

```text
.editorconfig
.gitattributes
.gitignore
.github/workflows/validate.yml
AGENTS.md
README.md
astro.config.mjs
package.json
package-lock.json
tsconfig.json
docs/
  current-site-audit.md
  milestone-1-report.md
scripts/
  validate.py
  test_validate.py
src/
  components/
    About.astro
    Contact.astro
    Footer.astro
    Header.astro
    Hero.astro
    Process.astro
    Services.astro
  layouts/BaseLayout.astro
  pages/index.astro
  scripts/site.js
  styles/global.css
```

New files: the Astro configuration/package files, component/layout/page sources,
and this report. CSS and JavaScript moved into `src/`; Git may display these as
renames. Modified files: README, AGENTS, both validator scripts, and CI. The legacy
root HTML was removed; no generated output, dependencies, screenshots, cache,
test proxy, environment secrets, or unrelated local files belong in the commit.

Commit title: `refactor: migrate site foundation to Astro`. The completion response
records the resulting SHA, origin branch equality, and final Git status because
a commit cannot contain its own hash. No upstream push, merge, or deployment is
part of this milestone. Milestone 2 has not been started.
