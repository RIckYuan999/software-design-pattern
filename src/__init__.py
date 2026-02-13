"""處方系統模組"""

from .domain import Case, Gender, Patient, Prescription
from .exceptions import (
    ConfigurationError,
    DiagnosisError,
    PatientNotFoundError,
    PrescriptionSystemError,
    StorageError,
)
from .facade import PrescriptionSystemFacade
from .handler import DiseaseHandler, HandlerRegistry
from .prescriber import PrescriptionRequest, PrescriptionResult, Prescriber
from .storage_strategy import StorageRegistry, StorageStrategy, register_storage

__all__ = [
    # Domain
    "Case",
    "Gender",
    "Patient",
    "Prescription",
    # Exceptions
    "ConfigurationError",
    "DiagnosisError",
    "PatientNotFoundError",
    "PrescriptionSystemError",
    "StorageError",
    # Facade
    "PrescriptionSystemFacade",
    # Handler
    "DiseaseHandler",
    "HandlerRegistry",
    # Prescriber
    "PrescriptionRequest",
    "PrescriptionResult",
    "Prescriber",
    # Storage
    "StorageRegistry",
    "StorageStrategy",
    "register_storage",
]
