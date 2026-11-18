from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import PaymentIn,PaymentOut,InvoiceOut
from app.services import PaymentService
router=APIRouter(prefix="/invoices/{invoice_id}/payments",tags=["Payments"])
@router.post("",status_code=201)
def create(invoice_id:int,p:PaymentIn,db:Session=Depends(get_db)):
    a,x=PaymentService(db).record(invoice_id,p.model_dump())
    return {"payment_attempt":PaymentOut.model_validate(a),"invoice":InvoiceOut.model_validate(x)}
