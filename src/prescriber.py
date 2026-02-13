from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Any, Awaitable

from .domain import Patient, Prescription
from .handler import DiseaseHandler, HandlerRegistry
from .logging_config import setup_logger

logger = setup_logger("prescriber")


@dataclass(slots=True)
class PrescriptionRequest:
    patient: Patient
    symptoms: list[str]
    context: dict[str, Any]


@dataclass(slots=True)
class PrescriptionResult:
    patient: Patient
    symptoms: list[str]
    prescription: Prescription | None
    context: dict[str, Any]

    @property
    def is_healthy(self) -> bool:
        return self.prescription is None



PrescriptionCallback = Callable[[PrescriptionResult], Awaitable[None] | None]



class Prescriber:

    __slots__ = (
        "_queue", "_active_rules", "_callback", "_running",
        "_workers", "_worker_count", "_prescriber_delay", "_processing_count",
        "_idle_event"
    )

    def __init__(self, worker_count: int = 1, prescriber_delay: float = 3.0) -> None:
        self._queue: asyncio.Queue[PrescriptionRequest] = asyncio.Queue()
        self._active_rules: list[DiseaseHandler] = []
        self._callback: PrescriptionCallback | None = None
        self._running: bool = False
        self._workers: list[asyncio.Task[None]] = []
        self._worker_count = worker_count
        self._prescriber_delay = prescriber_delay
        self._processing_count: int = 0
        self._idle_event = asyncio.Event()
        self._idle_event.set()

    def configure_rules(self, file_path: str | Path) -> None:
        path = Path(file_path)

        try:
            supported_diseases = {
                line.strip()
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            }
            self._active_rules = HandlerRegistry.get_by_names(supported_diseases)
            logger.info(f"Loaded {len(self._active_rules)} disease rules")
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {path}")

    def set_callback(self, callback: PrescriptionCallback) -> None:
        self._callback = callback

    async def add_request(
        self,
        patient: Patient,
        symptoms: list[str],
        context: dict[str, Any]
    ) -> None:
        self._idle_event.clear()
        request = PrescriptionRequest(
            patient=patient,
            symptoms=symptoms,
            context=context
        )
        await self._queue.put(request)

    def is_idle(self) -> bool:
        return self._queue.empty() and self._processing_count == 0

    async def wait_until_idle(self) -> None:
        await self._idle_event.wait()

    async def start(self) -> None:
        if self._running:
            return

        self._running = True
        self._workers = [
            asyncio.create_task(
                self._worker(worker_id),
                name=f"prescriber-worker-{worker_id}"
            )
            for worker_id in range(self._worker_count)
        ]
        logger.info(f"Started {self._worker_count} worker(s)")

    async def stop(self) -> None:

        await self._queue.join()
        self._running = False

        for worker in self._workers:
            worker.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("All workers stopped")

    async def __aenter__(self) -> Prescriber:
        await self.start()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.stop()


    async def _worker(self, worker_id: int) -> None:
        try:
            while True:
                request = await self._queue.get()
                self._processing_count += 1

                try:
                    await self._prescription(request)
                except asyncio.CancelledError:
                    raise
                except Exception as e:
                    logger.exception(f"Worker-{worker_id} error: {e}")
                finally:
                    self._processing_count -= 1
                    self._queue.task_done()
                    if self.is_idle():
                        self._idle_event.set()

        except asyncio.CancelledError:
            pass

    async def _prescription(self, request: PrescriptionRequest) -> None:
        await asyncio.sleep(self._prescriber_delay)

        prescription = None
        for rule in self._active_rules:
            if matched := rule.match(request.patient, request.symptoms):
                prescription = matched
                break

        if self._callback:
            result = PrescriptionResult(
                patient=request.patient,
                symptoms=request.symptoms,
                prescription=prescription,
                context=request.context
            )

            callback_result = self._callback(result)
            if asyncio.iscoroutine(callback_result):
                await callback_result
