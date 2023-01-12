import os
import json
from src import util
# import util

# with open('config.json') as f:
#     config = json.load(f)

# CUSTOM_HEADERS_ORIGIN = config['REQUEST_HEADER']

KIDSNOTE_LANG = {"Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}
# 쿠키 가져오기 더 나은 방법이 있을텐데 바쁘니 패스
KIDSNOTE_COOKIE = {"Cookie": str(util.getCookiesFromDomain(
    'kidsnote', '')).replace('{', '').replace('}', '').replace("'", '').replace(',', ';').replace(': ', '=')}

print(KIDSNOTE_COOKIE)

CUSTOM_HEADERS = dict(KIDSNOTE_LANG, **KIDSNOTE_COOKIE)

OUTPUT_ROOT = 'output/'

BASE_URL = 'https://www.kidsnote.com'
REPORT_URL = BASE_URL + '/reports' + '/'
ALNUMS_URL = BASE_URL + '/albums' + '/'
