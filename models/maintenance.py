from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class Maintenance(BaseModel):
    maintenance_id: str = Field(..., unique=True)
    service_impacted: List[str] = Field(...)
    organization_id: str = Field(...)
    maintenance_name: str = Field(...)
    maintenance_description: str = Field(...)
    maintenance_status: str = Field(default="Scheduled")
    start_from: datetime = Field(...)
    end_at: datetime = Field(...)
