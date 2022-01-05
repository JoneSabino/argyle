from __future__ import annotations
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import uuid

class EstBudget(BaseModel):
    min: float = 0.0
    max: float = 0.0

class Pendencies(BaseModel):
    suggested_action: str = ''
    percentage_value: int = 0


class Project(BaseModel):
    type: str = ''
    description: str = ''
    level: str = ''
    est_budget: Union[float, EstBudget] = 0.0
    est_duration: str = ''
    weekly_hours: str = ''
    skills: str = ''


class RecommendedJobs(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    title: str = ''
    featured: bool = False
    payment_verified: bool = False
    age: str = ''
    proposals: str = ''
    client_country: str = ''
    project: Project


class Profile(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    first_name: str = ''
    last_name: str = ''
    full_name: str = ''
    title: str = ''
    completeness_percentage: int = 0
    pendencies: Pendencies
    available_connects: int = 0
    visibility: str = ''
    availability: str = ''
    categories: List[str] = ['']
    recommended_jobs: Optional[List[RecommendedJobs]] = None


class Model(BaseModel):
    profile: Profile
