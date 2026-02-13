from __future__ import annotations

from datetime import datetime
from enum import Enum, auto
from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints, ConfigDict


Medicine = Annotated[str, StringConstraints(min_length=3, max_length=30, strip_whitespace=True)]
PatientId = Annotated[str, StringConstraints(pattern=r"^[A-Z][12]\d{8}$")]


class Gender(Enum):
    MALE = auto()
    FEMALE = auto()

class Prescription(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str = Field(min_length=4, max_length=30)
    potential_disease: str = Field(min_length=3, max_length=100)
    medicines: list[Medicine] = Field(default_factory=list)
    usage: str = Field(min_length=1, max_length=1000)


class Case(BaseModel):
    symptoms: list[str] = Field(default_factory=list)
    prescriptions: list[Prescription] = Field(default_factory=list)
    case_time: datetime = Field(default_factory=datetime.now)


class Patient(BaseModel):
    id: PatientId
    name: str = Field(min_length=1, max_length=30)
    gender: Gender
    age: int = Field(ge=1, le=180)
    height: int = Field(ge=1, le=500)
    weight: int = Field(ge=1, le=500)
    case: list[Case] = Field(default_factory=list)

    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return self.weight / (height_m ** 2)
