from src.models import Patient, Doctor, Schedule, VisitResult, User
from src.repositories import patient_repository as patients, doctor_repository as doctors, schedule_repository as schedules, appointment_repository as appointments, visit_result_repository as results, user_repository as users

def _required(*values):
    if any(not str(v or '').strip() for v in values): raise ValueError('Обязательные поля не могут быть пустыми')

def create_patient(last_name,first_name,patronymic,birth_date,oms_policy,phone=None):
    _required(last_name,first_name,birth_date,oms_policy)
    if any(p.oms_policy == oms_policy for p in patients.get_all()): raise ValueError('Пациент с таким полисом уже существует')
    return patients.create(Patient(None,last_name.strip(),first_name.strip(),(patronymic or '').strip() or None,birth_date.strip(),oms_policy.strip(),phone or None))
def create_doctor(last_name,first_name,patronymic,specialty,office):
    _required(last_name,first_name,specialty,office); return doctors.create(Doctor(None,last_name.strip(),first_name.strip(),(patronymic or '').strip() or None,specialty.strip(),office.strip()))
def create_schedule(doctor_id,start_at,end_at):
    if not doctors.get_by_id(doctor_id): raise ValueError('Врач не найден')
    if end_at <= start_at: raise ValueError('Время окончания должно быть позже начала')
    return schedules.create(Schedule(None,doctor_id,start_at,end_at))
def create_appointment(patient_id,schedule_id):
    if not patients.get_by_id(patient_id): raise ValueError('Пациент не найден')
    if not schedules.get_by_id(schedule_id): raise ValueError('Интервал приёма не найден')
    if any(a.schedule_id == schedule_id and a.status != 'cancelled' for a in appointments.get_all()): raise ValueError('Интервал уже занят')
    return appointments.create(patient_id,schedule_id)
def cancel_appointment(i):
    if not appointments.get_by_id(i): raise ValueError('Запись не найдена')
    appointments.update_status(i,'cancelled')
def complete_appointment(i):
    if not appointments.get_by_id(i): raise ValueError('Запись не найдена')
    appointments.update_status(i,'completed')
def add_result(appointment_id,conclusion,recommendations=None):
    _required(conclusion)
    a=appointments.get_by_id(appointment_id)
    if not a: raise ValueError('Запись не найдена')
    if results.get_by_appointment(appointment_id): raise ValueError('Результат уже существует')
    return results.create(VisitResult(None,appointment_id,conclusion.strip(),recommendations or None))
def authenticate(login,password):
    u=users.get_by_login(login); return u if u and u.password == password else None
def register(login,password,role='registrar'):
    _required(login,password)
    if users.get_by_login(login): raise ValueError('Такой логин уже существует')
    if role not in ('registrar','doctor'): raise ValueError('Недопустимая роль')
    return users.create(User(None,login,password,role))
