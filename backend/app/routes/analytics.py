from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Case


router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):
    total_cases = db.query(func.count(Case.id)).scalar()

    open_cases = (
        db.query(func.count(Case.id))
        .filter(Case.status == "open")
        .scalar()
    )

    in_progress_cases = (
        db.query(func.count(Case.id))
        .filter(Case.status == "in_progress")
        .scalar()
    )

    resolved_cases = (
        db.query(func.count(Case.id))
        .filter(Case.status == "resolved")
        .scalar()
    )

    high_priority_cases = (
        db.query(func.count(Case.id))
        .filter(Case.priority == "high")
        .scalar()
    )

    return {
        "total_cases": total_cases,
        "open_cases": open_cases,
        "in_progress_cases": in_progress_cases,
        "resolved_cases": resolved_cases,
        "high_priority_cases": high_priority_cases
    }

@router.get("/by-priority")
def cases_by_priority(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Case.priority,
            func.count(Case.id)
        )
        .group_by(Case.priority)
        .all()
    )

    return {
        priority: count
        for priority, count in results
    }

@router.get("/by-category")
def cases_by_category(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Case.category,
            func.count(Case.id)
        )
        .group_by(Case.category)
        .all()
    )

    return {
        category: count
        for category, count in results
    }

@router.get("/by-status")
def cases_by_status(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Case.status,
            func.count(Case.id)
        )
        .group_by(Case.status)
        .all()
    )

    return {
        status: count
        for status, count in results
    }

@router.get("/average-resolution-time")
def average_resolution_time(
    db: Session = Depends(get_db)
):
    average_seconds = (
        db.query(
            func.avg(
                func.extract(
                    "epoch",
                    Case.resolved_at - Case.created_at
                )
            )
        )
        .filter(Case.resolved_at.isnot(None))
        .scalar()
    )

    if average_seconds is None:
        return {
            "average_resolution_hours": None,
            "message": "No resolved cases available"
        }

    average_hours = average_seconds / 3600

    return {
        "average_resolution_hours": round(float(average_hours), 2)
    }
