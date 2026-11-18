from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class PlanIn(BaseModel):
    name:str; price:Decimal=Field(gt=0); currency:str="INR"; billing_interval:str="monthly"; is_active:bool=True
class PlanOut(ORM):
    id:int; name:str; price:Decimal; currency:str; billing_interval:str; is_active:bool
class PlanUpdate(BaseModel):
    is_active: bool
class CustomerIn(BaseModel): name:str; email:EmailStr
class CustomerOut(ORM): id:int; name:str; email:EmailStr; created_at:datetime
class SubscriptionIn(BaseModel): customer_id:int; plan_id:int; start_date:date|None=None
class SubscriptionOut(ORM): id:int; customer_id:int; plan_id:int; status:str; start_date:date; end_date:date|None
class InvoiceIn(BaseModel):
    subscription_id:int; period_start:date|None=None; period_end:date|None=None; due_date:date|None=None
class InvoiceOut(ORM):
    id:int; subscription_id:int; customer_id:int; amount_due:Decimal; amount_paid:Decimal
    currency:str; status:str; period_start:date; period_end:date; due_date:date; created_at:datetime
class PaymentIn(BaseModel):
    amount:Decimal=Field(gt=0); currency:str="INR"; status:str; provider_reference:str; failure_reason:str|None=None
class PaymentOut(ORM):
    id:int; invoice_id:int; amount:Decimal; currency:str; status:str; provider_reference:str
    failure_reason:str|None; created_at:datetime
class LedgerOut(ORM):
    id:int; customer_id:int; invoice_id:int|None; event_type:str; amount:Decimal
    currency:str; reference_id:str; description:str; created_at:datetime
