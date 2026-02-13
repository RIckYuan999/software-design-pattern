from __future__ import annotations


class PrescriptionSystemError(Exception):
    pass


class PatientNotFoundError(PrescriptionSystemError):
    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        super().__init__(f"Patient '{patient_id}' not found")


class ConfigurationError(PrescriptionSystemError):
    pass


class StorageError(PrescriptionSystemError):
    pass


class DiagnosisError(PrescriptionSystemError):
    pass
