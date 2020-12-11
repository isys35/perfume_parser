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




if __name__ == '__main__':
    update_descriptions()
