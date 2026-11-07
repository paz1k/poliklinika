from src.database import get_connection
from src.models import Appointment

def _map(r): return Appointment(r["appointment_id"],r["patient_id"],r["schedule_id"],r["status"],r["patient_name"] if "patient_name" in r.keys() else None,r["doctor_name"] if "doctor_name" in r.keys() else None,r["start_at"] if "start_at" in r.keys() else None)
def create(patient_id,schedule_id):
    with get_connection() as c:
        cur=c.execute("INSERT INTO appointments(patient_id,schedule_id) VALUES(?,?)",(patient_id,schedule_id)); return cur.lastrowid
def get_by_id(i):
    with get_connection() as c:
        r=c.execute("SELECT a.*,(p.last_name || ' ' || p.first_name || COALESCE(' ' || p.patronymic, '')) patient_name,(d.last_name || ' ' || d.first_name || COALESCE(' ' || d.patronymic, '')) doctor_name,s.start_at FROM appointments a JOIN patients p ON p.patient_id=a.patient_id JOIN schedule s ON s.schedule_id=a.schedule_id JOIN doctors d ON d.doctor_id=s.doctor_id WHERE a.appointment_id=?",(i,)).fetchone(); return _map(r) if r else None
def get_all():
    with get_connection() as c: return [_map(r) for r in c.execute("SELECT a.*,(p.last_name || ' ' || p.first_name || COALESCE(' ' || p.patronymic, '')) patient_name,(d.last_name || ' ' || d.first_name || COALESCE(' ' || d.patronymic, '')) doctor_name,s.start_at FROM appointments a JOIN patients p ON p.patient_id=a.patient_id JOIN schedule s ON s.schedule_id=a.schedule_id JOIN doctors d ON d.doctor_id=s.doctor_id ORDER BY s.start_at")]
def update_status(i,status):
    with get_connection() as c: c.execute("UPDATE appointments SET status=? WHERE appointment_id=?",(status,i))
def delete(i):
    with get_connection() as c: c.execute("DELETE FROM appointments WHERE appointment_id=?",(i,))
