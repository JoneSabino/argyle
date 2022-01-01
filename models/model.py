from __future__ import annotations
from typing import List, Optional, Union
from pydantic import BaseModel, Field
import uuid

class EstBudget(BaseModel):
    min: float
    max: float

class Pendencies(BaseModel):
    suggested_action: str
    percentage_value: int


class Project(BaseModel):
    type_: str
    description: str
    level: str
    est_budget: Optional[Union[float, EstBudget]] = 0.0
    est_duration: Optional[str] = ''
    weekly_hours: Optional[str] = ''
    skills: Optional[str] = ''


class RecommendedJobs(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    title: str
    featured: bool
    payment_verified: bool
    age: str
    proposals: str
    client_country: str
    project: Project


class Profile(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex)
    first_name: str
    last_name: str
    full_name: str
    title: str
    completeness_percentage: int
    pendencies: Pendencies
    available_connects: int
    visibility: str
    availability: str
    categories: List[str]
    recommended_jobs: List[RecommendedJobs]


class Model(BaseModel):
    profile: Profile
