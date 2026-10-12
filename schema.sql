PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    birth_date TEXT NOT NULL,
    oms_policy TEXT NOT NULL UNIQUE,
    phone TEXT
);

CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    office TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS schedule (
    schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctor_id INTEGER NOT NULL,
    start_at TEXT NOT NULL,
    end_at TEXT NOT NULL,
    CHECK (end_at > start_at),
    UNIQUE (doctor_id, start_at),
    FOREIGN KEY (doctor_id) REFERENCES doctors (doctor_id)
);

CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER NOT NULL,
    schedule_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'scheduled',
    CHECK (status IN ('scheduled', 'completed', 'cancelled')),
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id),
    FOREIGN KEY (schedule_id) REFERENCES schedule (schedule_id)
);

CREATE UNIQUE INDEX IF NOT EXISTS unique_active_appointment
ON appointments (schedule_id)
WHERE status != 'cancelled';

CREATE TABLE IF NOT EXISTS visit_results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    appointment_id INTEGER NOT NULL UNIQUE,
    conclusion TEXT NOT NULL,
    recommendations TEXT,
    FOREIGN KEY (appointment_id)
        REFERENCES appointments (appointment_id)
);