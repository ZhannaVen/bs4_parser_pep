from pathlib import Path


# URL's
MAIN_DOC_URL = 'https://docs.python.org/3/'
PEP_DOC_URL = 'https://peps.python.org/'

# Local Directories
BASE_DIR = Path(__file__).parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'parser.log'
RESULTS_DIR = BASE_DIR / 'results'

# Formats
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
DT_FORMAT = '%d.%m.%Y %H:%M:%S'

# Phrases
FILE_SAVED = 'Файл с результатами был сохранён: {}'
ERROR_RESPONSE = 'Возникла ошибка при загрузке страницы {}'

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
