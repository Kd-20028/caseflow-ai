from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CaseCreate(BaseModel):
    title: str
    description: str


class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str | None
    priority: str
    status: str
    sentiment: str | None
    ai_summary: str | None
    assigned_team: str | None
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    priority: str | None = None
    status: str | None = None
    assigned_team: str | None = None

