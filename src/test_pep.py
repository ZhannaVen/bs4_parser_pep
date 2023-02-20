
import requests_cache
from bs4 import BeautifulSoup
from constants import PEP_DOC_URL
from utils import get_response, find_tag

session = requests_cache.CachedSession()
response = get_response(session, PEP_DOC_URL)
soup = BeautifulSoup(response.text, 'lxml')
table_indexes = soup.find_all('section', attrs={'id': 'numerical-index'})
print(table_indexes)

