from src.database import get_connection
from src.models import Schedule

def _map(r): return Schedule(r["schedule_id"],r["doctor_id"],r["start_at"],r["end_at"],r["doctor_name"] if "doctor_name" in r.keys() else None)
def create(x):
    with get_connection() as c:
        cur=c.execute("INSERT INTO schedule(doctor_id,start_at,end_at) VALUES(?,?,?)",(x.doctor_id,x.start_at,x.end_at)); return Schedule(cur.lastrowid,x.doctor_id,x.start_at,x.end_at)
def get_by_id(i):
    with get_connection() as c:
        r=c.execute("SELECT s.*, (d.last_name || ' ' || d.first_name || COALESCE(' ' || d.patronymic, '')) doctor_name FROM schedule s JOIN doctors d ON d.doctor_id=s.doctor_id WHERE s.schedule_id=?",(i,)).fetchone(); return _map(r) if r else None
def get_all():
    with get_connection() as c: return [_map(r) for r in c.execute("SELECT s.*,(d.last_name || ' ' || d.first_name || COALESCE(' ' || d.patronymic, '')) doctor_name FROM schedule s JOIN doctors d ON d.doctor_id=s.doctor_id ORDER BY start_at")]
def delete(i):
    with get_connection() as c: c.execute("DELETE FROM schedule WHERE schedule_id=?",(i,))
