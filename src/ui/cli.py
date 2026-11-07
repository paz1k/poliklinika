from src.services import services as svc
from src.repositories import patient_repository as patients, doctor_repository as doctors, schedule_repository as schedules, appointment_repository as appointments, visit_result_repository as results
from src.export_data import export_all

def show_data():
    print('\nПациенты:')
    for p in patients.get_all(): print(f'{p.patient_id}. {p.full_name}, полис {p.oms_policy}, тел. {p.phone or "—"}')
    print('\nВрачи:')
    for d in doctors.get_all(): print(f'{d.doctor_id}. {d.full_name} — {d.specialty}, каб. {d.office}')
    print('\nРасписание:')
    for s in schedules.get_all(): print(f'{s.schedule_id}. {s.doctor_name}: {s.start_at}–{s.end_at}')
    print('\nЗаписи:')
    for a in appointments.get_all(): print(f'{a.appointment_id}. {a.start_at} — {a.patient_name}, {a.doctor_name}: {a.status}')

def registrar_menu():
    while True:
        print('\n=== Меню регистратора ===\n1. Показать данные\n2. Добавить пациента\n3. Записать пациента\n4. Отменить запись\n0. Выход')
        c=input('Выберите действие: ').strip()
        try:
            if c=='1': show_data()
            elif c=='2': svc.create_patient(input('Фамилия: '),input('Имя: '),input('Отчество: '),input('Дата рождения (ГГГГ-ММ-ДД): '),input('Полис ОМС: '),input('Телефон: ')); print('Пациент добавлен')
            elif c=='3': svc.create_appointment(int(input('ID пациента: ')),int(input('ID интервала: '))); print('Пациент записан')
            elif c=='4': svc.cancel_appointment(int(input('ID записи: '))); print('Запись отменена')
            elif c=='0': return
        except (ValueError,TypeError) as e: print(f'Ошибка: {e}')

def doctor_menu():
    while True:
        print('\n=== Меню врача ===\n1. Показать записи\n2. Завершить приём и внести результат\n0. Выход')
        c=input('Выберите действие: ').strip()
        try:
            if c=='1':
                for a in appointments.get_all(): print(f'{a.appointment_id}. {a.start_at} — {a.patient_name}: {a.status}')
            elif c=='2':
                i=int(input('ID записи: ')); svc.complete_appointment(i); svc.add_result(i,input('Заключение: '),input('Рекомендации: ')); print('Результат сохранён')
            elif c=='0': return
        except (ValueError,TypeError) as e: print(f'Ошибка: {e}')

def run():
    while True:
        print('\n=== Поликлиника ===\n1. Войти\n2. Зарегистрироваться\n3. Экспортировать записи в JSON/CSV/XML/YAML\n0. Выход')
        c=input('Выберите действие: ').strip()
        if c=='0': return
        try:
            if c=='1':
                u=svc.authenticate(input('Логин: '),input('Пароль: '))
                if not u: print('Неверный логин или пароль')
                elif u.role=='registrar': registrar_menu()
                else: doctor_menu()
            elif c=='2': svc.register(input('Логин: '),input('Пароль: ')); print('Регистрация выполнена')
            elif c=='3':
                for path in export_all(): print(f'Создан: {path.relative_to(svc.__dict__.get("PROJECT_DIR", path.parent.parent)) if False else path}')
        except (ValueError,TypeError) as e: print(f'Ошибка: {e}')
