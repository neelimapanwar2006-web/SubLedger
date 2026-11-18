from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import SubscriptionIn,SubscriptionOut
from app.services import SubscriptionService
router=APIRouter(prefix="/subscriptions",tags=["Subscriptions"])
@router.post("",response_model=SubscriptionOut,status_code=201)
def create(p:SubscriptionIn,db:Session=Depends(get_db)): return SubscriptionService(db).create(p.model_dump())
@router.get("",response_model=list[SubscriptionOut])
def listing(db:Session=Depends(get_db)): return SubscriptionService(db).all()
