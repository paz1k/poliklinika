from src.database import get_connection
from src.models import User

def _map(r): return User(r["user_id"],r["login"],r["password"],r["role"])
def get_by_login(login):
    with get_connection() as c:
        r=c.execute("SELECT * FROM users WHERE login=?",(login,)).fetchone(); return _map(r) if r else None
def create(user):
    with get_connection() as c:
        cur=c.execute("INSERT INTO users(login,password,role) VALUES(?,?,?)",(user.login,user.password,user.role)); return User(cur.lastrowid,user.login,user.password,user.role)
