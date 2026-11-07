from src.database import get_connection
from src.models import VisitResult

def _map(r): return VisitResult(r["result_id"],r["appointment_id"],r["conclusion"],r["recommendations"])
def create(x):
    with get_connection() as c:
        cur=c.execute("INSERT INTO visit_results(appointment_id,conclusion,recommendations) VALUES(?,?,?)",(x.appointment_id,x.conclusion,x.recommendations)); return VisitResult(cur.lastrowid,x.appointment_id,x.conclusion,x.recommendations)
def get_by_appointment(i):
    with get_connection() as c:
        r=c.execute("SELECT * FROM visit_results WHERE appointment_id=?",(i,)).fetchone(); return _map(r) if r else None
def get_all():
    with get_connection() as c: return [_map(r) for r in c.execute("SELECT * FROM visit_results ORDER BY result_id")]
def update(x):
    with get_connection() as c: c.execute("UPDATE visit_results SET conclusion=?,recommendations=? WHERE result_id=?",(x.conclusion,x.recommendations,x.result_id))
def delete(i):
    with get_connection() as c: c.execute("DELETE FROM visit_results WHERE result_id=?",(i,))
