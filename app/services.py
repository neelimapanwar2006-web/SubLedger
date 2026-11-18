from datetime import date,timedelta
from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.repositories import PlanRepo,CustomerRepo,SubscriptionRepo,InvoiceRepo,PaymentRepo,LedgerRepo
class PlanService:
    def __init__(self, db):
        self.r = PlanRepo(db)

    def create(self, d):
        if Decimal(d["price"]) <= 0:
            raise HTTPException(400, "Plan price must be greater than zero")
        return self.r.add(d)

    def all(self):
        return self.r.all()

    def update(self, plan_id, data):
        plan = self.r.get(plan_id)

        if not plan:
            raise HTTPException(404, "Plan not found")

        return self.r.update(plan, data)
class CustomerService:
    def __init__(self,db): self.r=CustomerRepo(db)
    def create(self,d):
        if self.r.email(d["email"]): raise HTTPException(409,"Customer email already exists")
        try: return self.r.add(d)
        except IntegrityError: self.r.db.rollback(); raise HTTPException(409,"Customer email already exists")
    def all(self): return self.r.all()
class SubscriptionService:
    def __init__(self,db): self.r=SubscriptionRepo(db); self.p=PlanRepo(db); self.c=CustomerRepo(db)
    def create(self,d):
        if not self.c.get(d["customer_id"]): raise HTTPException(404,"Customer not found")
        p=self.p.get(d["plan_id"])
        if not p: raise HTTPException(404,"Plan not found")
        if not p.is_active: raise HTTPException(400,"Cannot subscribe to inactive plan")
        if self.r.active(d["customer_id"],d["plan_id"]): raise HTTPException(409,"Active subscription already exists")
        d["start_date"]=d.get("start_date") or date.today()
        return self.r.add(d)
    def all(self): return self.r.all()
class LedgerService:
    def __init__(self,db): self.r=LedgerRepo(db)
    def record(self,**d): return self.r.add(d)
    def all(self): return self.r.all()
class InvoiceService:
    def __init__(self,db): self.db=db; self.s=SubscriptionRepo(db); self.p=PlanRepo(db); self.r=InvoiceRepo(db); self.l=LedgerService(db)
    def create(self,d):
        s=self.s.get(d["subscription_id"])
        if not s: raise HTTPException(404,"Subscription not found")
        if s.status!="active": raise HTTPException(400,"Subscription is not active")
        p=self.p.get(s.plan_id); start=d.get("period_start") or date.today(); end=d.get("period_end") or start+timedelta(days=30)
        if end<=start: raise HTTPException(400,"period_end must be after period_start")
        x=self.r.add(dict(subscription_id=s.id,customer_id=s.customer_id,amount_due=p.price,amount_paid=Decimal("0"),currency=p.currency,status="issued",period_start=start,period_end=end,due_date=d.get("due_date") or start+timedelta(days=7)))
        self.l.record(customer_id=s.customer_id,invoice_id=x.id,event_type="invoice_created",amount=x.amount_due,currency=x.currency,reference_id=f"invoice:{x.id}",description="Invoice generated")
        return x
    def all(self): return self.r.all()
class PaymentService:
    def __init__(self,db): self.r=InvoiceRepo(db); self.p=PaymentRepo(db); self.l=LedgerService(db)
    def record(self,i,d):
        x=self.r.get(i)
        if not x: raise HTTPException(404,"Invoice not found")
        st=d["status"].lower(); amt=Decimal(d["amount"])
        if st not in ("succeeded","failed"): raise HTTPException(400,"status must be succeeded or failed")
        if amt<=0: raise HTTPException(400,"Payment amount must be positive")
        if d["currency"].upper()!=x.currency.upper(): raise HTTPException(400,"Currency mismatch")
        remaining=x.amount_due-x.amount_paid
        if st=="succeeded" and (remaining<=0 or amt>remaining): raise HTTPException(400,"Payment exceeds remaining balance")
        attempt=self.p.add(dict(invoice_id=i,amount=amt,currency=d["currency"].upper(),status=st,provider_reference=d["provider_reference"],failure_reason=d.get("failure_reason")))
        if st=="succeeded":
            x.amount_paid+=amt; x.status="paid" if x.amount_paid==x.amount_due else "partially_paid"; self.r.save(x)
        self.l.record(customer_id=x.customer_id,invoice_id=i,event_type=f"payment_{st}",amount=amt,currency=x.currency,reference_id=d["provider_reference"],description=f"Payment {st}")
        return attempt,x
