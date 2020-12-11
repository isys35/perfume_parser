import optfarm_parser
import perfume_parser
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import ConnectionError, ChunkedEncodingError

HOST = 'https://randewoo.ru'
CSV_FILE = 'data_with_description.csv'


def _parse_notes(soup):
    dl_soup = soup.select_one('dl.dl')
    divs_soup = dl_soup.select('div')
    top_notes = None
    middle_notes = None
    base_notes = None
    for div_soup in divs_soup:
        if div_soup.select_one('dt').text == 'Верхние ноты':
            top_notes = div_soup.select_one('dd').text
        elif div_soup.select_one('dt').text == 'Средние ноты':
            middle_notes = div_soup.select_one('dd').text
        elif div_soup.select_one('dt').text == 'Базовые ноты':
            base_notes = div_soup.select_one('dd').text
    return top_notes, middle_notes, base_notes


def get_response(url):
    while True:
        try:
            response = requests.get(url)
            return response
        except (ConnectionError, ChunkedEncodingError):
            time.sleep(5)


def update_descriptions(start_index=None):
    try:
        data = optfarm_parser.load_data()
    except FileNotFoundError:
        optfarm_parser.parsing()
        data = optfarm_parser.load_data()
    if not start_index:
        optfarm_parser.write_header(CSV_FILE)
        start_index = 1
    for index, perfume_data in enumerate(data[start_index:]):
        print(index)
        full_name = "{} {}".format(perfume_data[1], perfume_data[25])
        print(full_name)
        search_text = quote(full_name)
        url = "{}/search?q={}".format(HOST, search_text)
        response_search = get_response(url)
        soup_search = BeautifulSoup(response_search.text, 'lxml')
        product_search_soup = soup_search.select_one('li.products__item.js-products__item.b-catalogItem')
        if product_search_soup:
            url_product = HOST + product_search_soup.select_one('a.b-catalogItem__photoWrap')['href']
            response_product = get_response(url_product)
            soup_product = BeautifulSoup(response_product.text, 'lxml')
            description_soup = soup_product.select_one('.collapsable')
            if description_soup:
                description = description_soup.text
                perfume_data[9] = "<p>{}</p>".format(description) + optfarm_parser.DESCRIPTION
                notes = _parse_notes(soup_product)
                if notes:
                    perfume_data[32], perfume_data[35], perfume_data[38] = notes
        else:
            perfume_data[9] = optfarm_parser.DESCRIPTION
        try:
            optfarm_parser.save_data([perfume_data], CSV_FILE)
        except UnicodeEncodeError:
            perfume_data[9] = optfarm_parser.DESCRIPTION
            optfarm_parser.save_data([perfume_data], CSV_FILE)


def get_not_updated_description_percent():
    data = optfarm_parser.load_data(CSV_FILE)
    count_not_updated_data = len([el for el in data if el[9] == optfarm_parser.DESCRIPTION])
    return int(100 * count_not_updated_data / len(data))


def updater():
    data = optfarm_parser.load_data(CSV_FILE)
    data[9807][9] = optfarm_parser.DESCRIPTION
    data[9807][1] = 'Hermes'
    data[9807][0] = 'Equipage Geranium (мужские) 100ml туалетная вода'
    data[9807][25] = 'Equipage Geranium'
    data[9807][26] = 'Equipage Geranium'
    data[9807][27] = 'Equipage Geranium'
    data[9807][28] = 'Equipage Geranium'
    data[9808][9] = optfarm_parser.DESCRIPTION
    data[9808][1] = 'Hermes'
    data[9808][0] = 'Equipage Geranium (мужские) 100ml туалетная вода'
    data[9808][25] = 'Equipage Geranium'
    data[9808][26] = 'Equipage Geranium'
    data[9808][27] = 'Equipage Geranium'
    data[9808][28] = 'Equipage Geranium'
    data[1539][9] = optfarm_parser.DESCRIPTION
    data[1539][1] = 'Atelier Boheme'
    data[1539][0] = 'Lea Aux Yeux Lilas Aimait Les Geraniums (женские) 15ml парфюмерная вода'
    data[1539][25] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1539][26] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1539][27] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1539][28] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'

    data[1540][9] = optfarm_parser.DESCRIPTION
    data[1540][1] = 'Atelier Boheme'
    data[1540][0] = 'Lea Aux Yeux Lilas Aimait Les Geraniums (женские) 15ml парфюмерная вода'
    data[1540][25] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1540][26] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1540][27] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'
    data[1540][28] = 'Lea Aux Yeux Lilas Aimait Les Geraniums'

    data[11304][9] = optfarm_parser.DESCRIPTION
    data[11304][1] = 'Jo Malone'
    data[11304][0] = 'Jo Malone Geranium & Verbena (унисекс) 30ml одеколон'
    data[11304][25] = 'Geranium & Verbena'
    data[11304][26] = 'Geranium & Verbena'
    data[11304][27] = 'Geranium & Verbena'
    data[11304][28] = 'Geranium & Verbena'

    optfarm_parser.save_data(data, 'data2.csv')

if __name__ == '__main__':
    updater()
