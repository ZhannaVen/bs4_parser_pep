import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from requests import HTTPError
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (ARCHIVE_SAVED, ARGS, BASE_DIR, DOWNLOADS_URL,
                       EXPECTED_STATUS, MAIN_DOC_URL, NOT_FOUND_404,
                       PARSER_ERROR, PARSER_FINISHED, PARSER_STARTED,
                       PEP_DOC_URL, UNEXPECTED_PEP_STATUS, UNKNOWN_STATUS,
                       WHATSNEW_URL)
from exceptions import ParserException
from outputs import control_output
from utils import find_tag, make_soup


def whats_new(session):
    soup = make_soup(session, WHATSNEW_URL)
    sections_by_python = soup.select(
        '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(sections_by_python):
        version_link = urljoin(WHATSNEW_URL, section.find('a')['href'])
        soup = make_soup(session, version_link)
        results.append(
            (
                version_link,
                find_tag(soup, 'h1').text,
                find_tag(soup, 'dl').text.replace('\n', ' ')
            ))
    return results


def latest_versions(session):
    soup = make_soup(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise HTTPError(NOT_FOUND_404)
    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append(
            (a_tag['href'], version, status)
        )
    return results


def download(session):
    soup = make_soup(session, DOWNLOADS_URL)
    pdf_a4_tag = soup.select_one('table.docutils td > [href$="pdf-a4.zip"]')
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_link)
    filename = archive_url.split('/')[-1]
    # пришлось убрать константу, иначе не проходят тесты
    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(ARCHIVE_SAVED.format(archive_path))


def pep(session):
    soup = make_soup(session, PEP_DOC_URL)
    section_tag = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    tbody_tag = find_tag(section_tag, 'tbody')
    tr_tags = tbody_tag.find_all('tr')
    results = defaultdict()
    for tag in tqdm(tr_tags):
        status_key = find_tag(tag, 'td').text[1:]
        expected_status = EXPECTED_STATUS.get(status_key, [])
        if not expected_status:
            logging.info(UNKNOWN_STATUS.format(status_key))
        pep_url = urljoin(PEP_DOC_URL, find_tag(tag, 'a')['href'])
        soup = make_soup(session, pep_url)
        dl_tag = find_tag(soup, 'dl')
        dt_parent = dl_tag.find(string='Status').find_parent()
        pep_status = dt_parent.next_sibling.next_sibling.string
        if pep_status in expected_status:
            results[pep_status] += 1
        else:
            logging.info(UNEXPECTED_PEP_STATUS.format(
                pep_url,
                pep_status,
                expected_status
            ))
    return [
        ('Статус', 'Количество'),
        *results.items(),
        ('Всего', sum(results.values())),
    ]


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
}


def main():
    configure_logging()
    logging.info(PARSER_STARTED)
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(ARGS.format(args))
    try:
        session = requests_cache.CachedSession()
        if args.clear_cache:
            session.cache.clear()
        parser_mode = args.mode
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except ParserException:
        logging.exception(
            PARSER_ERROR, stack_info=True, exc_info=True)
    logging.info(PARSER_FINISHED)


if __name__ == '__main__':
    main()
