from fastapi import FastAPI
from app.db import Base, engine
from app.routes import plans, customers, subscriptions, invoices, payments, ledger
Base.metadata.create_all(bind=engine)
app = FastAPI(title="SubLedger API", version="1.0.0")
for r in [plans.router, customers.router, subscriptions.router, invoices.router, payments.router, ledger.router]:
    app.include_router(r, prefix="/api")
@app.get("/health")
def health(): return {"status": "ok"}
