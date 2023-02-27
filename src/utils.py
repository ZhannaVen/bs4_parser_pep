from bs4 import BeautifulSoup
from requests import RequestException

from constants import ERROR_RESPONSE, TAG_NOT_FOUND
from exceptions import ParserFindTagException


def get_response(session, url, encoding='utf-8'):
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        raise ConnectionError(ERROR_RESPONSE.format(url))


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs={} if attrs is None else attrs)
    if searched_tag is None:
        raise ParserFindTagException(TAG_NOT_FOUND.format(tag, attrs))
    return searched_tag


def make_soup(session, url):
    response = get_response(session, url)
    return BeautifulSoup(response.text, features='lxml')
