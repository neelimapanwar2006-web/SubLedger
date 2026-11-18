from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import CustomerIn,CustomerOut
from app.services import CustomerService
router=APIRouter(prefix="/customers",tags=["Customers"])
@router.post("",response_model=CustomerOut,status_code=201)
def create(p:CustomerIn,db:Session=Depends(get_db)): return CustomerService(db).create(p.model_dump())
@router.get("",response_model=list[CustomerOut])
def listing(db:Session=Depends(get_db)): return CustomerService(db).all()
