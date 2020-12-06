import optfarm_parser
import perfume_parser
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup

HOST = 'https://randewoo.ru'
CSV_FILE = 'data_with_description.csv'


def update_descriptions(start_index=None):
    try:
        data = optfarm_parser.load_data()
    except FileNotFoundError:
        optfarm_parser.parsing()
        data = optfarm_parser.load_data()
    if not start_index:
        optfarm_parser.write_header(CSV_FILE)
        start_index = 1
    for perfume_data in data[start_index:]:
        full_name = "{} {}".format(perfume_data[1], perfume_data[25])
        print(full_name)
        search_text = quote(full_name)
        url = "{}/search?q={}".format(HOST, search_text)
        response_search = requests.get(url)
        soup_search = BeautifulSoup(response_search.text, 'lxml')
        product_search_soup = soup_search.select_one('li.products__item.js-products__item.b-catalogItem')
        if product_search_soup:
            url_product = HOST + product_search_soup.select_one('a.b-catalogItem__photoWrap')['href']
            response_product = requests.get(url_product)
            soup_product = BeautifulSoup(response_product.text, 'lxml')
            description = soup_product.select_one('.collapsable').text
            perfume_data[9] = description
        try:
            optfarm_parser.save_data([perfume_data], CSV_FILE)
        except UnicodeEncodeError:
            optfarm_parser.save_data([perfume_data], CSV_FILE, encoding='utf-8')


def get_not_updated_description_percent():
    data = optfarm_parser.load_data(CSV_FILE)
    count_not_updated_data = len([el for el in data if el[9] == optfarm_parser.DESCRIPTION])
    return int(100 * count_not_updated_data / len(data))


if __name__ == '__main__':
    update_descriptions()
