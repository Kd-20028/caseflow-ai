from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import SessionLocal
from app.models import Case
from app.schemas import CaseCreate, CaseResponse, CaseUpdate, Priority, Status, SortBy, SortOrder
from sqlalchemy import or_

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
    status: Status | None = None,
    priority: Priority | None = None,
    category: str | None = None,
    assigned_team: str | None = None,
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    sort_by: SortBy = SortBy.created_at,
    sort_order: SortOrder = SortOrder.desc,
    db: Session = Depends(get_db)
):
    query = db.query(Case)

    if status:
        query = query.filter(Case.status == status)

    if priority:
        query = query.filter(Case.priority == priority)

    if category:
        query = query.filter(Case.category == category)

    if assigned_team:
        query = query.filter(Case.assigned_team == assigned_team)

    if search:
        query = query.filter(
    or_(
        Case.title.ilike(f"%{search}%"),
        Case.description.ilike(f"%{search}%")
    )
)

    sortable_fields = {
    "created_at": Case.created_at,
    "priority": Case.priority,
    "status": Case.status,
    "title": Case.title,
}

    sort_column = sortable_fields.get(sort_by, Case.created_at)
    if sort_order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    return query.offset(skip).limit(limit).all()

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

    if case_data.status == Status.resolved:
        case.resolved_at = datetime.utcnow()

    elif case_data.status is not None and case_data.status != Status.resolved:
        case.resolved_at = None

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

