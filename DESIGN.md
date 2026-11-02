# IssueScope — API & Data Design

## API Endpoints

| Method | Path | Request body | Response | Auth | Notes |
|--------|------|-------------|----------|------|-------|
| `GET` | `/health` | — | `{status, app, environment}` | None | Liveness probe; must be fast, no LLM/DB calls |
| `POST` | `/chat` | `ChatRequest` | `ChatResponse` or SSE stream | API key (Week 4) | Calls primary model with fallback; set `stream:true` for SSE |
| `GET` | `/usage` | — | `UsageResponse` | None | Cumulative token + cost stats since last restart |
| `POST` | `/ask` | `AskRequest` | `AskResponse` | API key (Week 4) | RAG endpoint — retrieves chunks then calls LLM (Week 3) |

### Schema definitions

#### `ChatRequest`
```json
{
  "messages": [{"role": "user", "content": "string"}],
  "stream": false
}
```

#### `ChatResponse`
```json
{
  "answer": "string",
  "model_used": "gpt-4o-mini",
  "input_tokens": 120,
  "output_tokens": 340,
  "cost_usd": 0.000222
}
```

#### `UsageResponse`
```json
{
  "total_requests": 42,
  "total_input_tokens": 15000,
  "total_output_tokens": 42000,
  "total_cost_usd": 0.031500
}
```

#### `AskRequest` *(planned — Week 3)*
```json
{
  "question": "string",
  "top_k": 5
}
```

#### `AskResponse` *(planned — Week 3)*
```json
{
  "answer": "string",
  "citations": [
    {"document": "Sambcorp_DRHP.pdf", "page": 47, "excerpt": "string"}
  ],
  "model_used": "string",
  "cost_usd": 0.000450
}
```

---

## Database Tables

> Postgres 16 with the `pgvector` extension. All tables use `UUID` primary keys.

### `documents`

Tracks every ingested prospectus PDF.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` PK | `gen_random_uuid()` |
| `filename` | `TEXT` NOT NULL | Original filename |
| `source_url` | `TEXT` | Where the PDF was downloaded from |
| `pages` | `INTEGER` | Total page count |
| `sha256` | `TEXT` | SHA-256 hex digest for dedup |
| `downloaded_at` | `TIMESTAMPTZ` | Download timestamp |
| `processed_at` | `TIMESTAMPTZ` | Null until chunking + embedding complete |
| `status` | `TEXT` | `pending` \| `processing` \| `ready` \| `failed` |

### `chunks`

Stores text chunks with page provenance, ready for vector search.

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` PK | |
| `document_id` | `UUID` FK → `documents.id` | Cascade delete |
| `page_number` | `INTEGER` | Source page in the PDF |
| `heading` | `TEXT` | Nearest section heading (nullable) |
| `content` | `TEXT` NOT NULL | Raw chunk text |
| `embedding` | `VECTOR(1536)` | OpenAI `text-embedding-3-small` |
| `created_at` | `TIMESTAMPTZ` | |

### `usage_log`

Persistent per-request cost log (Week 3 — currently in-memory in `app/usage.py`).

| Column | Type | Notes |
|--------|------|-------|
| `id` | `UUID` PK | |
| `endpoint` | `TEXT` | `/chat` or `/ask` |
| `model_used` | `TEXT` | |
| `input_tokens` | `INTEGER` | |
| `output_tokens` | `INTEGER` | |
| `cost_usd` | `NUMERIC(12,8)` | |
| `created_at` | `TIMESTAMPTZ` | |

---

## Architecture Overview

```
Client
  │
  ▼
FastAPI (app/main.py)
  ├── GET  /health   ──► returns 200 immediately
  ├── POST /chat     ──► app/llm.py ──► OpenAI API (primary → fallback)
  │                       └── app/usage.py  (record tokens + cost)
  ├── GET  /usage    ──► app/usage.py (read snapshot)
  └── POST /ask  [Week 3]
        ├── pgvector similarity search  (chunks table)
        └── app/llm.py  (answer with retrieved context)

Infrastructure (docker-compose.yml)
  ├── api   — FastAPI + uvicorn (this repo)
  └── db    — pgvector/pgvector:pg16
```
