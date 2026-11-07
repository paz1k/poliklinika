"""Экспорт записей на приём в JSON, CSV, XML и YAML."""
import csv
import json
import sys
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, SubElement, ElementTree

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.database import PROJECT_DIR, get_connection

OUT_DIR = PROJECT_DIR / "out"


def load_appointments() -> list[dict[str, Any]]:
    query = """
        SELECT a.appointment_id, a.status,
               p.patient_id, p.last_name patient_last_name,
               p.first_name patient_first_name, p.patronymic patient_patronymic,
               s.schedule_id, s.start_at, s.end_at,
               d.doctor_id, d.last_name doctor_last_name,
               d.first_name doctor_first_name, d.patronymic doctor_patronymic,
               d.specialty, d.office
        FROM appointments a
        JOIN patients p ON p.patient_id = a.patient_id
        JOIN schedule s ON s.schedule_id = a.schedule_id
        JOIN doctors d ON d.doctor_id = s.doctor_id
        ORDER BY s.start_at
    """
    with get_connection() as conn:
        rows = conn.execute(query).fetchall()
    result = []
    for row in rows:
        result.append({
            "appointment_id": row["appointment_id"],
            "status": row["status"],
            "patient": {
                "id": row["patient_id"],
                "last_name": row["patient_last_name"],
                "first_name": row["patient_first_name"],
                "patronymic": row["patient_patronymic"],
            },
            "schedule": {
                "id": row["schedule_id"],
                "start_at": row["start_at"],
                "end_at": row["end_at"],
            },
            "doctor": {
                "id": row["doctor_id"],
                "last_name": row["doctor_last_name"],
                "first_name": row["doctor_first_name"],
                "patronymic": row["doctor_patronymic"],
                "specialty": row["specialty"],
                "office": row["office"],
            },
        })
    return result


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result = {}
        for key, item in value.items():
            result.update(flatten(item, f"{prefix}.{key}" if prefix else key))
        return result
    if isinstance(value, list):
        return {prefix: ";".join(map(str, value))}
    return {prefix: value}


def add_xml(parent: Element, name: str, value: Any) -> None:
    element = SubElement(parent, name)
    if isinstance(value, dict):
        for key, item in value.items():
            add_xml(element, key, item)
    elif isinstance(value, list):
        for item in value:
            add_xml(element, "item", item)
    elif value is not None:
        element.text = str(value)


def yaml_scalar(value: Any) -> str:
    if value is None: return "null"
    if isinstance(value, bool): return "true" if value else "false"
    if isinstance(value, (int, float)): return str(value)
    return json.dumps(str(value), ensure_ascii=False)


def to_yaml(value: Any, indent: int = 0) -> str:
    pad = " " * indent
    lines = []
    if isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list)):
                lines.append(f"{pad}{key}:")
                lines.append(to_yaml(item, indent + 2))
            else:
                lines.append(f"{pad}{key}: {yaml_scalar(item)}")
    elif isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                first = True
                for key, subitem in item.items():
                    prefix = f"{pad}- {key}:" if first else f"{pad}  {key}:"
                    if isinstance(subitem, (dict, list)):
                        lines.append(prefix)
                        lines.append(to_yaml(subitem, indent + 4))
                    else:
                        lines.append(f"{prefix} {yaml_scalar(subitem)}")
                    first = False
            else:
                lines.append(f"{pad}- {yaml_scalar(item)}")
    return "\n".join(lines)


def export_all(records: list[dict[str, Any]] | None = None) -> list[Path]:
    records = load_appointments() if records is None else records
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    json_path = OUT_DIR / "data.json"
    json_path.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")

    csv_path = OUT_DIR / "data.csv"
    flat_records = [flatten(record) for record in records]
    fieldnames = sorted({key for record in flat_records for key in record})
    with csv_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_records)

    xml_path = OUT_DIR / "data.xml"
    root = Element("appointments")
    for record in records:
        add_xml(root, "appointment", record)
    ElementTree(root).write(xml_path, encoding="utf-8", xml_declaration=True)

    yaml_path = OUT_DIR / "data.yaml"
    yaml_path.write_text(to_yaml(records) + "\n", encoding="utf-8")
    return [json_path, csv_path, xml_path, yaml_path]


if __name__ == "__main__":
    paths = export_all()
    print("Файлы экспорта созданы в папке out:")
    for path in paths:
        print(f"- {path.relative_to(PROJECT_DIR)}")
