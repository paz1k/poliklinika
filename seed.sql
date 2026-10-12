-- Вымышленные пациенты для проверки программы.
INSERT OR IGNORE INTO patients
    (patient_id, full_name, birth_date, oms_policy, phone)
VALUES
    (1, 'Иванов Иван Иванович', '1990-05-15',
     '1111111111111111', '+79990000001'),
    (2, 'Петрова Анна Сергеевна', '1985-09-22',
     '2222222222222222', '+79990000002'),
    (3, 'Сидоров Алексей Павлович', '2001-03-10',
     '3333333333333333', '+79990000003');

     INSERT OR IGNORE INTO doctors
    (doctor_id, full_name, specialty, office)
VALUES
    (1, 'Смирнова Елена Викторовна', 'Терапевт', '101'),
    (2, 'Кузнецов Андрей Николаевич', 'Хирург', '203'),
    (3, 'Орлова Мария Олеговна', 'Невролог', '305');

    INSERT OR IGNORE INTO schedule
    (schedule_id, doctor_id, start_at, end_at)
VALUES
    (1, 1, '2026-10-13 09:00', '2026-10-13 09:30'),
    (2, 1, '2026-10-13 09:30', '2026-10-13 10:00'),
    (3, 2, '2026-10-13 10:00', '2026-10-13 10:30'),
    (4, 3, '2026-10-13 11:00', '2026-10-13 11:30');

    INSERT OR IGNORE INTO appointments
    (appointment_id, patient_id, schedule_id, status)
VALUES
    (1, 1, 1, 'completed'),
    (2, 2, 3, 'completed'),
    (3, 3, 4, 'scheduled');

    INSERT OR IGNORE INTO visit_results
    (result_id, appointment_id, conclusion, recommendations)
VALUES
    (1, 1, 'Профилактический осмотр проведён.',
     'Плановый осмотр через год.'),
    (2, 2, 'Контрольный осмотр проведён.',
     'Повторный приём по назначению врача.');