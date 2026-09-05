# LaunchPoint Pros

The LaunchPoint Pros business website, being developed incrementally toward a
production-grade, conversion-focused, SEO-ready site.

## Repository purpose

This repository contains the public website and its development documentation.
Milestone 0 established the development foundation. Milestone 1 migrates the
existing homepage to Astro while preserving its content, styling, and behavior.
See [the historical static-site audit](docs/current-site-audit.md) for deferred
limitations and [the M1 verification report](docs/milestone-1-report.md) for migration evidence.

## Current architecture

Astro generates a static homepage from `src/pages/index.astro`, a shared layout,
and seven section components. `src/styles/global.css` preserves the baseline
stylesheet; `src/scripts/site.js` bundles the existing interactions with Three.js
r134, GSAP 3.12.2, and ScrollTrigger 3.12.2. These scripts are served locally from
the generated `dist/_astro/` assets. Outfit still loads from Google Fonts.

Direct dependencies are pinned: Astro 7.3.1, GSAP 3.12.2, Three.js 0.134.0;
development tooling uses @astrojs/check 0.9.10 and TypeScript 6.0.3.
No server adapter, backend, or deployment integration is configured.

The contact control intentionally still simulates success, logs the entered email,
and clears it after three seconds without submitting a lead. Existing business
statistics are not verified by repository evidence. Missing animation targets,
navigation highlight limitations, accessibility defects, and other audit findings
remain deferred; the extra closing section tag was removed during migration.

## Local development

From the repository root, use Node 22.12+ (CI uses Node 22), npm 9.6.5+, and
Python 3.11+ for repository checks:

```sh
npm ci
npm run dev -- --host 127.0.0.1
```

Open the local URL printed by Astro (normally <http://127.0.0.1:4321>).
Stop the server with Ctrl+C. To test production output:

```sh
npm run build
npm run preview -- --host 127.0.0.1
```

Internet access is needed for installation and Google Fonts. No global package
installation is required. In a restricted sandbox, use a temporary writable cache
with `npm ci --cache "$(mktemp -d)"`; prefix Astro commands with
`ASTRO_TELEMETRY_DISABLED=1` if its preferences directory is unavailable.

## Validation

```sh
npm run check
npm run build
python3 scripts/validate.py
python3 scripts/test_validate.py
node --check src/scripts/site.js
git diff --check
npm ls --depth=0
```

Build before running the validator; missing `dist/index.html` is an error.
GitHub Actions installs locked dependencies, checks and builds Astro, then runs
the Python validator and its tests on pushes and pull requests, with no deployment
or secrets.

The validator scans tracked and non-ignored untracked files, including new files
before staging, plus ignored build output. It requires the Astro source files,
checks literal placeholder links in components, and checks assembled HTML for
structure, duplicate IDs, and fragment targets across components. Safety errors
exit nonzero; markup and contact warnings identify deferred site issues.
It checks common credentials and local paths without printing matched values.
It is neither a complete secret scanner nor a full HTML validator, and it does not
scan Git history. Component checks do not interpret arbitrary Astro expressions;
rendered checks cover the current build, so rebuild after source changes. Review
staged content and history separately if a leak is suspected.
Warnings do not certify the site as production-ready or its contact flow as functional.

## Development workflow

`upstream/main` and local `main` represent the production baseline.
`feat/site-growth-redesign` is the current controlled integration branch.
`origin` points to the working repository; `upstream` points to the baseline repository.

Edit → validate → review diff → commit → push → PR. Review untracked files as well
as `git diff`. Keep changes scoped to the approved milestone. Never push directly
to upstream/main, force push, or rewrite published history. Commits and pushes
remain explicit user actions unless separately authorized.

## Agent workflow

Read [AGENTS.md](AGENTS.md) before working. Preserve behavior, verify claims, and
stop after the approved milestone.

## Security

Never commit secrets. Local environment files belong outside Git history.
`.env.example` may contain placeholders only and is still scanned.
The existing ignore rules cover macOS metadata, dependencies, build output,
environment secrets, and logs; ignored files must not be force-added.

## Planned direction and roadmap

Astro is the current architecture. M2 positioning and information architecture,
Cloudflare hosting, and all later milestones remain future work.

| Milestone | Focus |
| --- | --- |
| M0 | Development foundation — complete |
| M1 | Astro migration — complete |
| M2 | Positioning and information architecture |
| M3 | Design system |
| M4 | Homepage |
| M5 | Service and SEO architecture |
| M6 | Proof |
| M7 | Lead generation |
| M8 | Technical SEO |
| M9 | Performance and accessibility |
| M10 | Analytics |
| M11 | Deployment |
| M12 | Post-launch growth |
