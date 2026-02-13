from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from .domain import Patient, Case
from .exceptions import ConfigurationError
from .logging_config import setup_logger

logger = setup_logger("database")


class PatientDatabase:
    __slots__ = ("_patients",)

    def __init__(self) -> None:
        self._patients: dict[str, Patient] = {}

    def load_form_json(self, filepath: str | Path):
        path = Path(filepath)

        if not path.exists():
            raise ConfigurationError(f"Patient data file not found: {path}")

        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            self._patients = {
                p["id"]: Patient(
                    id=p["id"],
                    name=p["name"],
                    gender=p["gender"],
                    age=p["age"],
                    height=p["height"],
                    weight=p["weight"],
                )
                for p in data
            }
            logger.info(f"Loaded {len(self._patients)} patients")
        except (json.JSONDecodeError, KeyError) as e:
            raise ConfigurationError(f"Invalid patient data format: {e}") from e

    def get(self, patient_id: str) -> Patient | None:
        return self._patients.get(patient_id)

    def add_case(self, patient_id: str, case: Case) -> None:
        patient = self.get(patient_id)
        if patient:
            patient.case.append(case)
        else:
            from .exceptions import PatientNotFoundError
            raise PatientNotFoundError(patient_id)

    def __getitem__(self, patient_id: str) -> Patient:
        return self._patients[patient_id]

    def __contains__(self, patient_id: str) -> bool:
        return patient_id in self._patients

    def __len__(self) -> int:
        return len(self._patients)

    def __iter__(self) -> Iterator[Patient]:
        return iter(self._patients.values())
