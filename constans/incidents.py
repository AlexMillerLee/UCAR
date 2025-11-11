import datetime
def get_status():
    return ((0, "new"), (1, "processing"), (2, "completed"), (3, "fake"), (4, "unknown"))
def get_source():
    return ((0, "operator"), (1, "monitoring"), (2, "partner"), (3, "unknown"))


def parse_datetime(value):
    """
    Проверяет, что value — корректная дата.
    Возвращает объект datetime.datetime или None, если неверно.
    """
    if isinstance(value, datetime.datetime):
        return value
    elif isinstance(value, str):
        try:
            # Парсим строку в формате ISO 8601
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            return None
    else:
        return None