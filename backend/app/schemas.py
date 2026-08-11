from datetime import datetime

from pydantic import BaseModel, ConfigDict

from enum import Enum

class SortBy(str, Enum):
    created_at = "created_at"
    priority = "priority"
    status = "status"
    title = "title"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Status(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class CaseCreate(BaseModel):
    title: str
    description: str

class CaseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    priority: Priority | None = None
    status: Status | None = None
    assigned_team: str | None = None


class CaseResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str | None
    priority: Priority
    status: Status
    sentiment: str | None
    ai_summary: str | None
    assigned_team: str | None
    created_at: datetime
    resolved_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
