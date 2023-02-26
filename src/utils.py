import logging

from bs4 import BeautifulSoup
from requests import RequestException

from constants import ERROR_RESPONSE, TAG_NOT_FOUND, URL_NOT_FOUND, UTF_8
from exceptions import ErrorResponseException, ParserFindTagException


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


def make_soup(session, url):
    response = get_response(session, url)
    if response is None:
        logging.info(URL_NOT_FOUND.format(url))
        return
    return BeautifulSoup(response.text, 'lxml')
