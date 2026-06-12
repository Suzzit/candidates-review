from pydantic import BaseModel, Field


class ScoreCreate(BaseModel):
    category: str
    score: int = Field(ge=1, le=5)
    note: str | None = None


class NotesUpdate(BaseModel):
    internal_notes: str
