from pathlib import Path
from urllib.parse import urljoin

# URL's
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'
WHATSNEW_URL = urljoin(MAIN_DOC_URL, 'whatsnew/')
DOWNLOADS_URL = urljoin(MAIN_DOC_URL, 'download.html')

# Local Directories
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = BASE_DIR / 'results'
DOWNLOADS_DIR = BASE_DIR / 'downloads'

# Formats
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

# Phrases
FILE_SAVED = 'Файл с результатами был сохранён: {}'
ARCHIVE_SAVED = 'Архив был загружен и сохранён: {}'
ERROR_RESPONSE = 'Возникла ошибка при загрузке страницы {}'
TAG_NOT_FOUND = 'Не найден тег {} {}'
NOT_FOUND_404 = 'Ничего не нашлось'
UNEXPECTED_PEP_STATUS = (
    'Несовпадающие статусы: {},'
    'cтатус в карточке: {},'
    'ожидаемые статусы: {}'
)
PARSER_STARTED = 'Парсер запущен!'
ARGS = 'Аргументы командной строки: {}'
PARSER_FINISHED = 'Парсер завершил работу.'
UNKNOWN_STATUS = 'Неизвестный статус: {}'
PARSER_ERROR = 'Ошибка в ходе работы парсера: {}'
URL_NOT_FOUND = 'По этому адресу ничего не нашлось: {}'

# Other
UTF_8 = 'utf-8'
PRETTY = 'pretty'
FILE = 'file'
EXPECTED_STATUS = {
        'A': ['Accepted', 'Active'],
        'D': ['Deferred'],
        'F': ['Final'],
        'P': ['Provisional'],
        'R': ['Rejected'],
        'S': ['Superseded'],
        'W': ['Withdrawn'],
        '': ['Draft']
}
