# Agent operating contract

## Project purpose and milestone boundaries

LaunchPoint Pros is being developed into a production-grade, conversion-focused,
SEO-ready business website. The current site uses Astro to generate static HTML,
with global CSS and bundled client JavaScript. Cloudflare hosting is a future milestone.

- Work incrementally within the explicitly approved milestone; never start future milestones automatically.
- Prefer small, reviewable changes and preserve working behavior unless explicitly tasked otherwise.
- Avoid unnecessary dependencies and unrelated cleanup.
- Use mobile-first, accessibility-aware, semantic HTML and progressive enhancement.
- Keep performance in mind and business claims grounded in verified information.
- Milestone 0 is the historical static baseline. Milestone 1 migrates that baseline
  to Astro with visual and behavioral parity; content and product changes remain deferred.

## Git safety

- Work only on the current approved feature branch unless instructed otherwise.
- Never push directly to upstream/main. Never force push or rewrite published history.
- Never delete or reset user work without explicit approval.
- Do not commit or push merely because edits were made. A task or milestone prompt
  may explicitly authorize commits and pushes. When authorized, complete the lifecycle:
  inspect → implement → validate → review diff → commit → push → verify.
- Do not delegate routine Git work to the user unless authentication or permissions block it.
- Never merge into upstream unless explicitly authorized in a future task.
- Keep commits scoped and descriptive. Do not make unrelated cleanup changes.
- Never commit credentials, API keys, secret environment files, local absolute paths,
  temporary editor state, or system metadata. Example environment files must contain placeholders only.

## Business and content integrity

Never invent customers, testimonials, case studies, revenue, conversion results,
project counts, satisfaction percentages, years of experience, certifications,
partnerships, locations, addresses, phone numbers, or awards.
Flag existing unverified claims rather than silently treating them as fact.

## SEO

- Do not create mass-generated SEO pages or doorway pages, keyword-stuff, hide text
  for search engines, or add misleading schema, fake reviews, or ratings.
- SEO changes must serve actual users and preserve crawlable semantic content.

## Accessibility

- Preserve keyboard operability and visible focus states; use semantic elements.
- Maintain appropriate form labels and avoid mouse-only interaction patterns.
- Respect prefers-reduced-motion wherever motion exists.

## Performance

- Do not add heavy libraries without justification; prefer native browser capabilities.
- Defer non-critical enhancement, avoid layout shifts, and minimize third-party scripts.

## Validation and completion

- Use Node 22.12+ and Python 3.11+. Install with npm ci, then run npm run check,
  npm run build, python3 scripts/validate.py, python3 scripts/test_validate.py,
  node --check src/scripts/site.js, and git diff --check before claiming completion.
- Build before repository validation: the validator checks Astro sources and the
  assembled dist/index.html and scans generated assets. Never commit dist/ or node_modules/.
- Inspect git diff and git status, including new untracked files.
- Verify relevant behavior in a local browser when available; distinguish static
  observations from measured results and record actual tested viewport dimensions.
- Report errors, warnings, skipped checks, and limitations honestly. Never claim
  an unrun test passed. Review docs/current-site-audit.md for deferred defects.
- Stop at the approved milestone. Do not deploy without an explicit deployment task.
