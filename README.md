# LaunchPoint Pros

The LaunchPoint Pros business website, being developed incrementally toward a
production-grade, conversion-focused, SEO-ready site.

## Repository purpose

This repository contains the public website and its development documentation.
Milestone 0 establishes the foundation without changing the existing homepage.
See [the current-site audit](docs/current-site-audit.md) for known limitations.

## Current architecture

A static homepage: `index.html`, `styles.css`, and `script.js`. There is no build
step, framework, package manifest, or installed runtime dependency.
The browser currently loads Outfit from Google Fonts and Three.js r134,
GSAP 3.12.2, and ScrollTrigger 3.12.2 from cdnjs. These are external runtime
dependencies; network/CDN failures can affect enhancement and interaction.

The contact control simulates success and does not submit leads to a backend.
Existing business statistics are not verified by repository evidence.

## Local development

From the repository root, with Python 3.11 or later:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open <http://127.0.0.1:8000>. Stop the server with Ctrl+C. Internet access is
needed for the existing CDN scripts and fonts. No global package install is needed.

## Validation

```sh
python3 scripts/validate.py
python3 scripts/test_validate.py
node --check script.js
git diff --check
```

The validator needs Python 3.11+ and Git; Node is optional for the separate
JavaScript syntax check. GitHub Actions runs the Python validator on pushes and
pull requests, with no deployment or secrets.

The validator scans tracked and non-ignored untracked files, including new files
before staging. Safety errors exit nonzero; warnings identify deferred site issues.
It checks common credentials and local paths without printing matched values.
It is neither a complete secret scanner nor a full HTML validator, and it does not
scan Git history. Review staged content and history separately if a leak is suspected.
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

Astro migration and Cloudflare hosting are planned future work, not implemented.

| Milestone | Focus |
| --- | --- |
| M0 | Development foundation |
| M1 | Astro migration |
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
