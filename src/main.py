import sqlite3
from pathlib import Path

# Папка проекта — на один уровень выше папки src.
project_dir = Path(__file__).resolve().parent.parent

# Подключаемся к базе. Если файла нет, SQLite создаст его.
connection = sqlite3.connect(project_dir / "poliklinika.db")

try:
    connection.execute("PRAGMA foreign_keys = ON")

    # Читаем описание таблиц и выполняем SQL-команды.
    schema = (project_dir / "schema.sql").read_text(encoding="utf-8")
    connection.executescript(schema)

    # Загружаем тестовые данные.
    seed = (project_dir / "seed.sql").read_text(encoding="utf-8")
    connection.executescript(seed)
    connection.commit()

    # Проверяем количество записей в каждой таблице.
    print("Количество записей:")
    for table_name in (
        "patients", "doctors", "schedule",
        "appointments", "visit_results"
    ):
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        ).fetchone()[0]
        print(f"- {table_name}: {count}")

    # Проверяем, какие таблицы созданы.
    tables = connection.execute(
        "SELECT name FROM sqlite_master "
        "WHERE type = 'table' AND name NOT LIKE 'sqlite_%' "
        "ORDER BY name"
    ).fetchall()

    print("Учёт пациентов в поликлинике")
    print("База данных подключена. Таблицы:")
    for table in tables:
        print("-", table[0])
finally:
    connection.close()