# SubLedger – SaaS Billing Backend

FastAPI + SQLAlchemy + PostgreSQL billing foundation with plans, customers, subscriptions, invoices, payment attempts and ledger events.

## Run locally (SQLite)
Python 3.12+:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Run with Docker/PostgreSQL
```bash
docker compose up --build
```
API: http://localhost:8000; Swagger: http://localhost:8000/docs; PostgreSQL host port: 5434.

## Tests
```bash
pytest -q
```

## APIs
| Method | Endpoint | Description |
|---|---|---|
| GET/POST | `/api/plans` | List/create plans |
| PATCH | `/api/plans/{plan_id}` | Activate/deactivate a plan |
| GET/POST | `/api/customers` | List/create customers |
| GET/POST | `/api/subscriptions` | List/create subscriptions |
| GET/POST | `/api/invoices` | List/generate invoices |
| POST | `/api/invoices/{invoice_id}/payments` | Record payment |
| GET | `/api/ledger` | List ledger entries |
| GET | `/health` | Health check |

## Example workflow
Create plan -> create customer -> create subscription -> generate invoice -> record payment -> inspect ledger.

See [DESIGN.md](DESIGN.md) for ERD, architecture, responsibilities, rule ownership and core flows.

## Assumptions/limitations
Payment attempts are simulated. No authentication, gateway integration, taxes, refunds, proration, recurring scheduler or idempotency support. Production hardening should add migrations, transactional service operations and concurrency controls.

## Submission checklist
- [ ] Run API and inspect Swagger.
- [ ] Run tests and verify passing output.
- [ ] Add Swagger/test screenshots if useful.
- [ ] Push this folder to a GitHub repository.
