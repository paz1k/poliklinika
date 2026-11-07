from src.database import get_connection
from src.models import Patient

def _map(r): return Patient(r['patient_id'],r['last_name'],r['first_name'],r['patronymic'],r['birth_date'],r['oms_policy'],r['phone'])
def create(x):
    with get_connection() as c:
        q=c.execute('INSERT INTO patients(last_name,first_name,patronymic,birth_date,oms_policy,phone) VALUES(?,?,?,?,?,?)',(x.last_name,x.first_name,x.patronymic,x.birth_date,x.oms_policy,x.phone)); return Patient(q.lastrowid,x.last_name,x.first_name,x.patronymic,x.birth_date,x.oms_policy,x.phone)
def get_by_id(i):
    with get_connection() as c:
        r=c.execute('SELECT * FROM patients WHERE patient_id=?',(i,)).fetchone(); return _map(r) if r else None
def get_all():
    with get_connection() as c: return [_map(r) for r in c.execute('SELECT * FROM patients ORDER BY last_name,first_name')]
def update(x):
    with get_connection() as c: c.execute('UPDATE patients SET last_name=?,first_name=?,patronymic=?,birth_date=?,oms_policy=?,phone=? WHERE patient_id=?',(x.last_name,x.first_name,x.patronymic,x.birth_date,x.oms_policy,x.phone,x.patient_id))
def delete(i):
    with get_connection() as c: c.execute('DELETE FROM patients WHERE patient_id=?',(i,))
