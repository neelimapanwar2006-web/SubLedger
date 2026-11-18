from datetime import datetime, date
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Plan(Base):
    __tablename__="plans"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(120), unique=True)
    price: Mapped[Decimal]=mapped_column(Numeric(12,2))
    currency: Mapped[str]=mapped_column(String(3), default="INR")
    billing_interval: Mapped[str]=mapped_column(String(20), default="monthly")
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    subscriptions: Mapped[list["Subscription"]]=relationship(back_populates="plan")
class Customer(Base):
    __tablename__="customers"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(160))
    email: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    subscriptions: Mapped[list["Subscription"]]=relationship(back_populates="customer")
    invoices: Mapped[list["Invoice"]]=relationship(back_populates="customer")
    ledger_entries: Mapped[list["LedgerEntry"]]=relationship(back_populates="customer")
class Subscription(Base):
    __tablename__="subscriptions"
    id: Mapped[int]=mapped_column(primary_key=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id"))
    plan_id: Mapped[int]=mapped_column(ForeignKey("plans.id"))
    status: Mapped[str]=mapped_column(String(20), default="active")
    start_date: Mapped[date]=mapped_column(Date, default=date.today)
    end_date: Mapped[date|None]=mapped_column(Date, nullable=True)
    customer: Mapped["Customer"]=relationship(back_populates="subscriptions")
    plan: Mapped["Plan"]=relationship(back_populates="subscriptions")
    invoices: Mapped[list["Invoice"]]=relationship(back_populates="subscription")
class Invoice(Base):
    __tablename__="invoices"
    id: Mapped[int]=mapped_column(primary_key=True)
    subscription_id: Mapped[int]=mapped_column(ForeignKey("subscriptions.id"))
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id"))
    amount_due: Mapped[Decimal]=mapped_column(Numeric(12,2))
    amount_paid: Mapped[Decimal]=mapped_column(Numeric(12,2), default=Decimal("0"))
    currency: Mapped[str]=mapped_column(String(3), default="INR")
    status: Mapped[str]=mapped_column(String(24), default="issued")
    period_start: Mapped[date]=mapped_column(Date)
    period_end: Mapped[date]=mapped_column(Date)
    due_date: Mapped[date]=mapped_column(Date)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    subscription: Mapped["Subscription"]=relationship(back_populates="invoices")
    customer: Mapped["Customer"]=relationship(back_populates="invoices")
    payment_attempts: Mapped[list["PaymentAttempt"]]=relationship(back_populates="invoice")
    ledger_entries: Mapped[list["LedgerEntry"]]=relationship(back_populates="invoice")
class PaymentAttempt(Base):
    __tablename__="payment_attempts"
    id: Mapped[int]=mapped_column(primary_key=True)
    invoice_id: Mapped[int]=mapped_column(ForeignKey("invoices.id"))
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    currency: Mapped[str]=mapped_column(String(3))
    status: Mapped[str]=mapped_column(String(20))
    provider_reference: Mapped[str]=mapped_column(String(120), unique=True)
    failure_reason: Mapped[str|None]=mapped_column(Text, nullable=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    invoice: Mapped["Invoice"]=relationship(back_populates="payment_attempts")
class LedgerEntry(Base):
    __tablename__="ledger_entries"
    id: Mapped[int]=mapped_column(primary_key=True)
    customer_id: Mapped[int]=mapped_column(ForeignKey("customers.id"))
    invoice_id: Mapped[int|None]=mapped_column(ForeignKey("invoices.id"), nullable=True)
    event_type: Mapped[str]=mapped_column(String(40))
    amount: Mapped[Decimal]=mapped_column(Numeric(12,2))
    currency: Mapped[str]=mapped_column(String(3))
    reference_id: Mapped[str]=mapped_column(String(120), index=True)
    description: Mapped[str]=mapped_column(String(255))
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)
    customer: Mapped["Customer"]=relationship(back_populates="ledger_entries")
    invoice: Mapped["Invoice"]=relationship(back_populates="ledger_entries")
