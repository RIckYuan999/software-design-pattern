from __future__ import annotations

from abc import ABC, abstractmethod
from typing import ClassVar

from .domain import Patient, Prescription, Gender


class DiseaseHandler(ABC):

    disease_name: ClassVar[str]

    @classmethod
    def get_disease_name(cls) -> str:
        return cls.disease_name

    @abstractmethod
    def match(self, patient: Patient, symptoms: list[str]) -> Prescription | None:
        pass

    @staticmethod
    def _normalize_symptoms(symptoms: list[str]) -> frozenset[str]:
        return frozenset(s.casefold() for s in symptoms)

class Covid19Handler(DiseaseHandler):

    disease_name = "COVID-19"
    _required_symptoms = frozenset({"headache", "cough"})

    def match(self, patient: Patient, symptoms: list[str]) -> Prescription | None:
        symptom_set = self._normalize_symptoms(symptoms)

        if self._required_symptoms.issubset(symptom_set):
            return Prescription(
                name="清冠一號",
                potential_disease="新冠肺炎（專業學名：COVID-19）",
                medicines=["清冠一號"],
                usage="相關藥材裝入茶包裡，使用500 mL 溫、熱水沖泡悶煮1~3 分鐘後即可飲用。",
            )
        return None


class AttractiveHandler(DiseaseHandler):

    disease_name = "Attractive"

    def match(self, patient: Patient, symptoms: list[str]) -> Prescription | None:
        symptom_set = self._normalize_symptoms(symptoms)

        is_young_female = patient.age == 18 and patient.gender == Gender.FEMALE
        has_sneeze = "sneeze" in symptom_set

        if is_young_female and has_sneeze:
            return Prescription(
                name="青春抑制劑",
                potential_disease="有人想你了 (專業學名：Attractive)",
                medicines=["假鬢角", "臭味噴霧"],
                usage="把假鬢角黏在臉的兩側，讓自己異性緣差一點，自然就不會有人想妳了。",
            )
        return None


class SleepApneaSyndromeHandler(DiseaseHandler):

    disease_name = "SleepApneaSyndrome"
    _bmi_threshold = 26.0

    def match(self, patient: Patient, symptoms: list[str]) -> Prescription | None:
        symptom_set = self._normalize_symptoms(symptoms)

        is_overweight = patient.bmi > self._bmi_threshold
        has_snore = "snore" in symptom_set

        if is_overweight and has_snore:
            return Prescription(
                name="打呼抑制劑",
                potential_disease="睡眠呼吸中止症（專業學名：SleepApneaSyndrome）",
                medicines=["一捲膠帶"],
                usage="睡覺時，撕下兩塊膠帶，將兩塊膠帶交錯黏在關閉的嘴巴上，就不會打呼了。",
            )
        return None


class HandlerRegistry:

    _instance: ClassVar[HandlerRegistry | None] = None
    _handlers: ClassVar[dict[str, type[DiseaseHandler]]] = {}

    def __new__(cls) -> HandlerRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def register(cls, handler_cls: type[DiseaseHandler]) -> type[DiseaseHandler]:
        cls._handlers[handler_cls.disease_name] = handler_cls
        return handler_cls

    @classmethod
    def get_all(cls) -> list[DiseaseHandler]:
        return [handler_cls() for handler_cls in cls._handlers.values()]

    @classmethod
    def get_by_names(cls, names: set[str]) -> list[DiseaseHandler]:
        return [
            handler_cls()
            for name, handler_cls in cls._handlers.items()
            if name in names
        ]


HandlerRegistry.register(Covid19Handler)
HandlerRegistry.register(AttractiveHandler)
HandlerRegistry.register(SleepApneaSyndromeHandler)


def get_all_handlers() -> list[DiseaseHandler]:
    return HandlerRegistry.get_all()
