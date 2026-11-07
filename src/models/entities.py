from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    patient_id: Optional[int]
    last_name: str
    first_name: str
    patronymic: Optional[str]
    birth_date: str
    oms_policy: str
    phone: Optional[str] = None
    @property
    def full_name(self): return ' '.join(x for x in (self.last_name, self.first_name, self.patronymic) if x)

@dataclass
class Doctor:
    doctor_id: Optional[int]
    last_name: str
    first_name: str
    patronymic: Optional[str]
    specialty: str
    office: str
    @property
    def full_name(self): return ' '.join(x for x in (self.last_name, self.first_name, self.patronymic) if x)

@dataclass
class Schedule:
    schedule_id: Optional[int]
    doctor_id: int
    start_at: str
    end_at: str
    doctor_name: Optional[str] = None

@dataclass
class Appointment:
    appointment_id: Optional[int]
    patient_id: int
    schedule_id: int
    status: str = 'scheduled'
    patient_name: Optional[str] = None
    doctor_name: Optional[str] = None
    start_at: Optional[str] = None

@dataclass
class VisitResult:
    result_id: Optional[int]
    appointment_id: int
    conclusion: str
    recommendations: Optional[str] = None

@dataclass
class User:
    user_id: Optional[int]
    login: str
    password: str
    role: str
