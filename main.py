from __future__ import annotations

import asyncio
import json
from pathlib import Path

from src.facade import PrescriptionSystemFacade
from src.domain import Case
from src.exceptions import PatientNotFoundError
from src.logging_config import get_logger
from src.storage_strategy import StorageStrategy, register_storage

logger = get_logger("main")


class XmlStorageStrategy(StorageStrategy):
    extension = ".xml"

    def save(self, case: Case, filename: str) -> Path:
        file_path = self._prepare_path(filename)

        with file_path.open("a", encoding="utf-8") as f:
            f.write("<case>\n")
            f.write(f"  <case_time>{case.case_time}</case_time>\n")
            f.write(f"  <symptoms>{case.symptoms}</symptoms>\n")
            f.write("  <prescriptions>\n")

            for prescription in case.prescriptions:
                f.write("    <prescription>\n")
                f.write(f"      <name>{prescription.name}</name>\n")
                f.write(f"      <potential_disease>{prescription.potential_disease}</potential_disease>\n")
                f.write(f"      <medicines>{prescription.medicines}</medicines>\n")
                f.write(f"      <usage>{prescription.usage}</usage>\n")
                f.write("    </prescription>\n")

            f.write("  </prescriptions>\n")
            f.write("</case>\n")

        logger.info(f"Saved (XML) -> {file_path}")
        return file_path


register_storage("xml", XmlStorageStrategy)




def setup_test_data() -> None:
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    patients = [
        {"id": "A223456789", "name": "Alice", "gender": 2, "age": 18, "height": 160, "weight": 50},
        {"id": "B123456789", "name": "Bob", "gender": 1, "age": 40, "height": 175, "weight": 85},
        {"id": "C123456780", "name": "Charlie", "gender": 1, "age": 25, "height": 180, "weight": 70},
    ]

    (data_dir / "patients.json").write_text(
        json.dumps(patients, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    diseases = ["COVID-19", "Attractive", "SleepApneaSyndrome"]
    (data_dir / "diseases.txt").write_text("\n".join(diseases), encoding="utf-8")


async def main() -> None:
    setup_test_data()

    async with PrescriptionSystemFacade(
        patient_json="data/patients.json",
        disease_txt="data/diseases.txt",
        worker_count=2,
        diagnosis_delay=3.0
    ) as system:
        test_cases = [
            ("A223456789", ["sneeze"], "output/2026/reports/alice", "json"),
            ("B123456789", ["snore", "Headache"], "output/backup/bob", "csv"),
            ("C123456780", ["Headache", "Cough"], "output/xml_logs/charlie", "xml"),
        ]

        for patient_id, symptoms, save_to, fmt in test_cases:
            try:
                await system.prescribe(patient_id, symptoms, save_to, fmt)
            except PatientNotFoundError as e:
                logger.error(str(e))

if __name__ == "__main__":
    asyncio.run(main())
