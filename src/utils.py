import logging

from requests import RequestException

from exceptions import ParserFindTagException, ErrorResponseException
from constants import UTF_8, ERROR_RESPONSE, TAG_NOT_FOUND


def get_response(session, url, coding=UTF_8):
    try:
        response = session.get(url)
        response.encoding = coding
        return response
    except RequestException:
        raise ErrorResponseException(ERROR_RESPONSE.format(url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs={} if attrs is None else attrs)
    if searched_tag is None:
        raise ParserFindTagException(TAG_NOT_FOUND.format(tag, attrs))
    return searched_tag
