from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class OrganizationModel(BaseModel):
    organization_id: str = Field(..., unique=True)
    organization_name: str = Field(..., unique=True)
    organization_slug: str = Field(..., unique=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
