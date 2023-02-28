class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class ParserFindListException(Exception):
    """Вызывается, когда парсер не может найти список."""
    pass


class ParserFindStatusException(Exception):
    """Вызывается, когда парсер не может найти список."""
    pass


class ErrorResponseException(Exception):
    """Вызывается, когда возникла ошибка при загрузке страницы."""
    pass


class ParserException(Exception):
    """Вызывается, когда возникла ошибка в ходе работы парсера."""
    pass
