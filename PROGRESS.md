# Progress

Commit after every class. Tag every Friday: `git tag week-N && git push origin week-N`.

## Week 1 (tag week-1 by Fri 23 Oct)
- [x] Repo created from the Examate template and registered on the form
- [x] README top section filled from my project card
- [x] /health runs locally
- [x] docs/QUESTIONS.md: 10 real questions
- [x] 50+ pages collected, DATASET.md filled, sample in data/sample/
- [x] Tag week-1 pushed

## Week 2 (tag week-2 by Fri 30 Oct)
- [x] POST /chat calls an LLM and returns structured JSON
- [x] Streaming, timeouts, retry and a fallback model
- [x] Cost log + GET /usage
- [x] Docker Compose (API + Postgres/pgvector) runs
- [x] CI green, live link in README
- [x] Tag week-2 pushed

## Week 3 (tag week-3 by Fri 6 Nov)
- [ ] Parser keeps page numbers and headings
- [ ] 500+ pages chunked, embedded and stored in pgvector
- [ ] POST /ask answers with [document, page] citations
- [ ] docs/EVAL_v0.md with my 10 questions scored
- [ ] Tag week-3 pushed

## Daily log
| Date | What I did today | Commit |
|---|---|---|
| 21 Oct 2026 | Repo set up from Examate template, README written, /health endpoint added | a7c37fd |
| 22 Oct 2026 | Added download tool, urls.txt | 3aeb499 |
| 02 Nov 2026 | Completed week 1: filled QUESTIONS.md and DATASET.md, pushed week-1 tag | 3fdc191 |
| 02 Nov 2026 | Week 2: POST /chat with OpenAI fallback + streaming, GET /usage, Docker Compose, DESIGN.md, updated CI | 44984b1 |
| 03 Nov 2026 | Fix: added pythonpath to pytest config so CI can find app module | 15fc540 |
| 03 Nov 2026 | Docker smoke test job added, CI test passing | 0704158 |
| 03 Nov 2026 | Fix: added psycopg import and JSONResponse to main.py, psycopg to requirements | 8857eec |
| 03 Nov 2026 | Configured pre-commit hooks, updated project settings | d384076 |
| 04 Nov 2026 | Fix CI docker-smoke: /ready curl no longer fails on 503 when no DB in CI | 860753e |
| 04 Nov 2026 | Deployed to Render, added live link to README | 16b9525 |
