class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ErrorResponseException(Exception):
    """Вызывается, когда возникла ошибка при загрузке страницы."""
    pass


class ParserException(Exception):
    """Вызывается, когда возникла ошибка в ходе работы парсера."""
    pass
