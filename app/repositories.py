from app import models
class Repo:
    def __init__(self,db): self.db=db
class PlanRepo(Repo):
    def get(self,i):
        return self.db.get(models.Plan,i)

    def all(self):
        return self.db.query(models.Plan).all()

    def add(self,d):
        x=models.Plan(**d)
        self.db.add(x)
        self.db.commit()
        self.db.refresh(x)
        return x

    def update(self, plan, data):
        for key, value in data.items():
            setattr(plan, key, value)
        self.db.commit()
        self.db.refresh(plan)
        return plan
class CustomerRepo(Repo):
    def get(self,i): return self.db.get(models.Customer,i)
    def email(self,e): return self.db.query(models.Customer).filter_by(email=e).first()
    def all(self): return self.db.query(models.Customer).all()
    def add(self,d):
        x=models.Customer(**d); self.db.add(x); self.db.commit(); self.db.refresh(x); return x
class SubscriptionRepo(Repo):
    def get(self,i): return self.db.get(models.Subscription,i)
    def active(self,c,p): return self.db.query(models.Subscription).filter_by(customer_id=c,plan_id=p,status="active").first()
    def all(self): return self.db.query(models.Subscription).all()
    def add(self,d):
        x=models.Subscription(**d); self.db.add(x); self.db.commit(); self.db.refresh(x); return x
class InvoiceRepo(Repo):
    def get(self,i): return self.db.get(models.Invoice,i)
    def all(self): return self.db.query(models.Invoice).all()
    def add(self,d):
        x=models.Invoice(**d); self.db.add(x); self.db.commit(); self.db.refresh(x); return x
    def save(self,x): self.db.add(x); self.db.commit(); self.db.refresh(x); return x
class PaymentRepo(Repo):
    def add(self,d):
        x=models.PaymentAttempt(**d); self.db.add(x); self.db.commit(); self.db.refresh(x); return x
class LedgerRepo(Repo):
    def add(self,d):
        x=models.LedgerEntry(**d); self.db.add(x); self.db.commit(); self.db.refresh(x); return x
    def all(self): return self.db.query(models.LedgerEntry).order_by(models.LedgerEntry.id.desc()).all()
