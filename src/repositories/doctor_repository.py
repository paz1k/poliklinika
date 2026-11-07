from src.database import get_connection
from src.models import Doctor

def _map(r): return Doctor(r['doctor_id'],r['last_name'],r['first_name'],r['patronymic'],r['specialty'],r['office'])
def create(x):
    with get_connection() as c:
        q=c.execute('INSERT INTO doctors(last_name,first_name,patronymic,specialty,office) VALUES(?,?,?,?,?)',(x.last_name,x.first_name,x.patronymic,x.specialty,x.office)); return Doctor(q.lastrowid,x.last_name,x.first_name,x.patronymic,x.specialty,x.office)
def get_by_id(i):
    with get_connection() as c:
        r=c.execute('SELECT * FROM doctors WHERE doctor_id=?',(i,)).fetchone(); return _map(r) if r else None
def get_all():
    with get_connection() as c: return [_map(r) for r in c.execute('SELECT * FROM doctors ORDER BY last_name,first_name')]
def update(x):
    with get_connection() as c: c.execute('UPDATE doctors SET last_name=?,first_name=?,patronymic=?,specialty=?,office=? WHERE doctor_id=?',(x.last_name,x.first_name,x.patronymic,x.specialty,x.office,x.doctor_id))
def delete(i):
    with get_connection() as c: c.execute('DELETE FROM doctors WHERE doctor_id=?',(i,))
