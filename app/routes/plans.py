from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import PlanIn, PlanOut, PlanUpdate
from app.services import PlanService

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.post("/", response_model=PlanOut, status_code=201)
def create(p: PlanIn, db: Session = Depends(get_db)):
    return PlanService(db).create(p.model_dump())


@router.get("/", response_model=list[PlanOut])
def listing(db: Session = Depends(get_db)):
    return PlanService(db).all()


@router.patch("/{plan_id}", response_model=PlanOut)
def update(
    plan_id: int,
    p: PlanUpdate,
    db: Session = Depends(get_db)
):
    return PlanService(db).update(plan_id, p.model_dump())