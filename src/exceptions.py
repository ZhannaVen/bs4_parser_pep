class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ErrorResponseException(Exception):
    """Вызывается, когда возникла ошибка при загрузке страницы."""
    pass


