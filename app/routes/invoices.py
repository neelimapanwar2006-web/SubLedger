from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import InvoiceIn,InvoiceOut
from app.services import InvoiceService
router=APIRouter(prefix="/invoices",tags=["Invoices"])
@router.post("",response_model=InvoiceOut,status_code=201)
def create(p:InvoiceIn,db:Session=Depends(get_db)): return InvoiceService(db).create(p.model_dump())
@router.get("",response_model=list[InvoiceOut])
def listing(db:Session=Depends(get_db)): return InvoiceService(db).all()
