# Agno Finance Agents (Equity Research Showcase)

Production-grade multi-agent (Agno) setup with memory, ReAct reasoning, self-critique, and strong guardrails. Ships a FastAPI demo for event showfloor.

## Quickstart

1. **Python 3.11+** and **git** installed.
2. Create env:

   ```bash
   #py -3.11 -m venv .venv && source .\.venv\Scripts\Activate.ps1
   #pip install -U pip
   #pip install -e .

   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt

   ```

3. Copy `.env.example` → `.env` and set `OPENAI_API_KEY`.
4. Run API:
   ```bash
   uvicorn apps.api.main:app --host 127.0.0.1 --port 8787 --access-log --log-level debug
   ```
5. POST an analysis:

   ```bash
   curl -X POST http://localhost:8787/v1/health  # For health check

   curl -X POST http://localhost:8787/v1/analyze      -H "Content-Type: application/json"      -d '{"ticker":"BBAS3.SA","prompt":"Full deep-dive with catalysts."}'
   ```

## Architecture

- **Agno Teams (collaborate)** orchestrated synthesis.
- **Persistent Memory** via Agno storage (SQLite by default).
- **Guardrails**: PI sanitization, ticker validation, domain allow-list, step/time caps.
- **ReAct** reasoning & self-critique via `ReasoningTools`.

## Extending

- Add more agents in `agents/` and register in `team_orchestrator.py`.
- Swap storage DB in `core/memory.py` (`AGNO_DB_URL`).
- Add knowledge/RAG later via Agno vector DBs (Qdrant, Weaviate, Couchbase, etc.).

## License

MIT

## Web UI (Django + buildless React)

This repository includes a minimal Django app that serves a React single-page UI (no Node needed).  
The UI calls the FastAPI backend at `http://localhost:8787/v1/analyze`.

### Run

In one terminal (backend):

```bash
uvicorn apps.api.main:app --host 127.0.0.1 --port 8787 --access-log --log-level debug
```

In another terminal (web UI):

```bash
python apps/web/manage.py migrate
python apps/web/manage.py runserver 9000
```

Open http://localhost:9000/

### Notes

- React/ReactDOM are imported via ESM from esm.sh, so you don't need Node or bundlers.
- To change the API base URL, edit `apps/web/dashboard/static/dashboard/app.umd.js`.

Screenshot:
![alt text](image.png)
