from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Case
from app.schemas import CaseCreate, CaseResponse, CaseUpdate


router = APIRouter(
    prefix="/cases",
    tags=["cases"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=CaseResponse)
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db)
):
    new_case = Case(
        title=case_data.title,
        description=case_data.description
    )

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case

@router.get("/", response_model=list[CaseResponse])
def get_cases(
    db: Session = Depends(get_db)
):
    cases = db.query(Case).all()

    return cases

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case

@router.patch("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    case_data: CaseUpdate,
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    update_data = case_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)

    return case

@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == case_id).first()

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    db.delete(case)
    db.commit()

    return {
        "message": "Case deleted successfully"
    }
