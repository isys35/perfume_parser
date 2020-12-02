import os
import json
import perfume_parser
import requests
from bs4 import BeautifulSoup
import re

URL = 'https://optparf.ru/'
BRENDS_FILE = 'brends.json'

if os.path.isfile(BRENDS_FILE):
    with open(BRENDS_FILE, 'r', encoding='utf-8') as json_file:
        BRENDS = json.load(json_file)
else:
    BRENDS = perfume_parser.get_brends()
    perfume_parser.save_json(BRENDS, BRENDS_FILE)

if __name__ == '__main__':
    response = requests.get(URL)
    soup = BeautifulSoup(response.text,'lxml')
    rows = soup.select('.row.table-body')
    for row in rows:
        cols_auto = row.select('.col-auto')
        cols = row.select('.col')
        article = cols_auto[0].text
        all_text = cols[0].text
        brend = None
        for BREND in BRENDS:
            if BREND in all_text:
                brend = BREND
                break
        if brend:
            all_text = all_text.split(brend, maxsplit=1)[-1].strip()
        print(all_text)
