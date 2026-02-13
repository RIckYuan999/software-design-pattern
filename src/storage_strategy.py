from __future__ import annotations

import csv
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar

from .domain import Case, Prescription
from .exceptions import StorageError
from .logging_config import setup_logger

logger = setup_logger("storage")


class StorageStrategy(ABC):

    extension: ClassVar[str]

    def _prepare_path(self, raw_path: str, extension: str | None = None) -> Path:
        ext = extension or self.extension
        path = Path(raw_path)

        if path.suffix.lower() != ext:
            path = path.with_suffix(ext)

        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @abstractmethod
    def save(self, case: Case, filename: str) -> Path:
        ...


class JsonStorageStrategy(StorageStrategy):

    extension = ".json"

    def save(self, case: Case, filename: str) -> Path:
        file_path = self._prepare_path(filename)

        try:
            with file_path.open("a", encoding="utf-8") as f:
                f.write(case.model_dump_json())
            logger.info(f"Saved (JSON) -> {file_path}")
            return file_path
        except IOError as e:
            raise StorageError(f"Failed to save JSON: {e}") from e


class CsvStorageStrategy(StorageStrategy):

    extension = ".csv"

    def save(self, case: Case, filename: str) -> Path:
        file_path = self._prepare_path(filename)
        exists = file_path.exists()

        case_fields = [f for f in Case.model_fields.keys() if f != "prescriptions"]
        prescription_fields = list(Prescription.model_fields.keys())
        header = case_fields + prescription_fields

        try:
            with file_path.open("a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                if not exists:
                    writer.writerow(header)

                for prescription in case.prescriptions:
                    case_values = [getattr(case, f) for f in case_fields]
                    prescription_values = [getattr(prescription, f) for f in prescription_fields]
                    writer.writerow(case_values + prescription_values)

            logger.info(f"Saved (CSV) -> {file_path}")
            return file_path
        except IOError as e:
            raise StorageError(f"Failed to save CSV: {e}") from e

class StorageRegistry:

    _instance: ClassVar[StorageRegistry | None] = None
    _strategies: ClassVar[dict[str, type[StorageStrategy]]] = {}
    _default: ClassVar[type[StorageStrategy]] = JsonStorageStrategy

    def __new__(cls) -> StorageRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, format_key: str, strategy_cls: type[StorageStrategy]) -> None:
        cls._strategies[format_key.lower()] = strategy_cls

    @classmethod
    def get(cls, format_key: str) -> StorageStrategy:
        strategy_cls = cls._strategies.get(format_key.lower())

        if strategy_cls is None:
            logger.warning(f"Format '{format_key}' not supported. Defaulting to JSON.")
            return cls._default()

        return strategy_cls()

    @classmethod
    def supported_formats(cls) -> list[str]:
        return list(cls._strategies.keys())


StorageRegistry.register("json", JsonStorageStrategy)
StorageRegistry.register("csv", CsvStorageStrategy)


def register_storage(format_key: str, cls: type[StorageStrategy]) -> None:
    StorageRegistry.register(format_key, cls)


def get_storage(format_key: str) -> StorageStrategy:
    return StorageRegistry.get(format_key)
