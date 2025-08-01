from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, JSON


class NylasMessage(SQLModel, table=True):
    __tablename__ = "nylas_messages"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    submitter: str
    data: dict = Field(sa_type=JSON)
    created_at: datetime = Field(default_factory=datetime.now)