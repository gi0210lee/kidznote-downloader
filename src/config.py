import json

with open('config.json') as f:
    config = json.load(f)

CUSTOM_HEADERS = config['REQUEST_HEADER']

OUTPUT_ROOT = 'output/'

BASE_URL = 'https://www.kidsnote.com'
REPORT_URL = BASE_URL + '/reports' + '/'
ALNUMS_URL = BASE_URL + '/albums' + '/'
