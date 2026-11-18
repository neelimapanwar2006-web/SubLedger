from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import LedgerOut
from app.services import LedgerService
router=APIRouter(prefix="/ledger",tags=["Ledger"])
@router.get("",response_model=list[LedgerOut])
def listing(db:Session=Depends(get_db)): return LedgerService(db).all()
