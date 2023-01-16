import os
import json

OUTPUT_ROOT = 'output/'
OUTPUT_ALBUMS = OUTPUT_ROOT + 'albums/'
OUTPUT_REPORTS = OUTPUT_ROOT + 'report/'

BASE_URL = 'https://www.kidsnote.com/'
REPORT_URL = BASE_URL + 'reports/'
ALNUMS_URL = BASE_URL + 'albums/'
LOGIN_URL = BASE_URL + 'login'
OLD_VER_URL = BASE_URL + 'home/'

CONST_DELAY_TIME = 1

# create to config.json
# {
#   "username": "",
#   "password": ""
# }

with open('config.json') as f:
    json_obj = json.load(f)

USERNAME = json_obj['username']
PASSWORD = json_obj['password']
