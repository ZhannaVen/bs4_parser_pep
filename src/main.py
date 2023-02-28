import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (ARCHIVE_SAVED, ARGS, BASE_DIR, DOWNLOADS, DOWNLOADS_URL,
                       EXPECTED_STATUS, MAIN_DOC_URL, NOT_FOUND_404,
                       PARSER_ERROR, PARSER_FINISHED, PARSER_STARTED,
                       PEP_DOC_URL, UNEXPECTED_PEP_STATUS, UNKNOWN_STATUS,
                       URL_NOT_FOUND, WHATSNEW_URL)
from exceptions import ParserFindListException
from outputs import control_output
from utils import find_tag, make_soup


def whats_new(session):
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    logs = []
    for section in tqdm(
        make_soup(
            session, WHATSNEW_URL
        ).select(
            '#what-s-new-in-python div.toctree-wrapper li.toctree-l1'
        )
    ):
        version_link = urljoin(WHATSNEW_URL, section.find('a')['href'])
        try:
            soup = make_soup(session, version_link)
            results.append(
                (
                    version_link,
                    find_tag(soup, 'h1').text,
                    find_tag(soup, 'dl').text.replace('\n', ' ')
                ))
        except ConnectionError:
            logs.append(URL_NOT_FOUND.format(version_link))
    for log in logs:
        logging.info(log)
    return results


def latest_versions(session):
    for ul in make_soup(
        session, MAIN_DOC_URL
    ).select(
        'div.sphinxsidebarwrapper ul'
    ):
        if 'All versions' in ul.text:
            a_tags = ul.find_all('a')
            break
    else:
        raise ParserFindListException(NOT_FOUND_404)
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
    pdf_a4_tag = make_soup(
        session, DOWNLOADS_URL
    ).select_one(
        'table.docutils td > [href$="pdf-a4.zip"]'
    )
    archive_url = urljoin(DOWNLOADS_URL, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    downloads_dir = BASE_DIR / DOWNLOADS
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(ARCHIVE_SAVED.format(archive_path))


def pep(session):
    results = defaultdict(int)
    logs = []
    for tag in tqdm(
        make_soup(
            session, PEP_DOC_URL
        ).select(
            '#numerical-index tbody tr'
        )
    ):
        status_key = find_tag(tag, 'td').text[1:]
        expected_status = EXPECTED_STATUS.get(status_key, [])
        if not expected_status:
            logs.append(UNKNOWN_STATUS.format(status_key))
        pep_url = urljoin(PEP_DOC_URL, find_tag(tag, 'a')['href'])
        try:
            dl_tag = find_tag(make_soup(session, pep_url), 'dl')
            dt_parent = dl_tag.find(string='Status').find_parent()
            pep_status = dt_parent.next_sibling.next_sibling.string
        except ConnectionError:
            logs.append(URL_NOT_FOUND.format(pep_url))
            continue
        if pep_status in expected_status:
            results[pep_status] += 1
        else:
            logs.append(UNEXPECTED_PEP_STATUS.format(
                pep_url,
                pep_status,
                expected_status
            ))
    for log in logs:
        logging.info(log)
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
    except Exception as exception:
        logging.exception(PARSER_ERROR.format(exception))
    logging.info(PARSER_FINISHED)


if __name__ == '__main__':
    main()
