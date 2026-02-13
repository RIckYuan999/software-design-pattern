from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Generator

from .database import PatientDatabase
from .domain import Case
from .exceptions import PatientNotFoundError
from .logging_config import get_logger
from .prescriber import Prescriber, PrescriptionResult
from .storage_strategy import StorageRegistry

logger = get_logger("facade")


class PrescriptionSystemFacade:

    __slots__ = ("_db", "_prescriber")

    def __init__(
        self,
        patient_json: str | Path,
        disease_txt: str | Path,
        worker_count: int = 1,
        diagnosis_delay: float = 3.0
    ) -> None:

        self._db = PatientDatabase()
        self._db.load_form_json(patient_json)

        self._prescriber = Prescriber(
            worker_count=worker_count,
            prescriber_delay=diagnosis_delay
        )
        self._prescriber.configure_rules(disease_txt)
        self._prescriber.set_callback(self._on_diagnosis_complete)


    async def prescribe(
        self,
        patient_id: str,
        symptoms: list[str],
        save_to: str | Path,
        output_format: str = "json"
    ) -> None:
        patient = self._db.get(patient_id)

        if patient is None:
            logger.warning(f"Patient {patient_id} not found")
            raise PatientNotFoundError(patient_id)

        logger.info(f"Request accepted for {patient.name}. Queuing...")

        await self._prescriber.add_request(
            patient=patient,
            symptoms=symptoms,
            context={"file": str(save_to), "fmt": output_format}
        )

    async def wait_until_idle(self) -> None:
        await self._prescriber.wait_until_idle()

    async def start(self) -> None:
        logger.info("=== Async Prescription System Started ===\n")
        await self._prescriber.start()

    async def shutdown(self) -> None:
        await self._prescriber.stop()
        logger.info("\n=== All tasks completed ===")

    async def __aenter__(self) -> PrescriptionSystemFacade:
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        logger.info("\nRequests sent. Processing in background...")
        await self.wait_until_idle()
        await self.shutdown()
    
    def __await__(self) -> Generator[Any, None, PrescriptionSystemFacade]:
        async def _startup() -> PrescriptionSystemFacade:
            await self.start()
            return self
        return _startup().__await__()

    async def _on_diagnosis_complete(self, result: PrescriptionResult) -> None:
        if result.is_healthy:
            logger.info(f"{result.patient.name} is healthy")
            return

        new_case = Case(
            symptoms=result.symptoms,
            case_time=datetime.now(),
            prescriptions=[result.prescription]
        )
        self._db.add_case(result.patient.id, new_case)

        storage = StorageRegistry.get(result.context.get("fmt", "json"))
        storage.save(new_case, result.context.get("file"))
