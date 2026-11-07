def require_id(value):
    if value is None:
        raise ValueError("Не удалось определить идентификатор записи")
    return value
