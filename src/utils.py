import logging

from requests import RequestException

from exceptions import ParserFindTagException, ErrorResponseException
from constants import UTF_8, ERROR_RESPONSE


def get_response(session, url, coding=UTF_8):
    try:
        response = session.get(url)
        response.encoding = coding
        return response
    except RequestException:
        raise ErrorResponseException(ERROR_RESPONSE.format(url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
