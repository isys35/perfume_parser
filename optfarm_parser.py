import os
import json
import perfume_parser
import requests
from bs4 import BeautifulSoup
import re
import csv

URL = 'https://optparf.ru/'
BRENDS_FILE = 'brends.json'
CSV_FILE = 'data.csv'

CSV_HEADER = ['name : Название', 'vendor : Производитель', 'image : Иллюстрация', 'pre_order : Предзаказ',
              'article : Артикул', 'folder : Категория', 'kind_id : ID', 'is_kind : Модификация',
              'note : Анонс товара', 'body : Описание', 'amount : Количество', 'amount_min : Мин. кол-во',
              'amount_multiplicity : Кратность', 'unit : Единица измерения', 'weight : Вес',
              'weight_unit : Единица веса', 'new : Новинка', 'special : Спецпредложение', 'yml : Yandex.Market',
              'price : Цена', 'price_old : Старая цена', 'price2 : Цена 2', 'price3 : Цена 3', 'currency : Валюта',
              'seo_noindex : Индексация', 'seo_h1 : Заголовок (H1)', 'seo_title : Title',
              'seo_description : Description', 'seo_keywords : Keywords', 'sef_url : ЧПУ', 'uuid : UUID Товара',
              'uuid_mod : UUID Модификации', 'cf_verhnie_noty : Верхние ноты', 'cf_klassifikacia : Классификация',
              'cf_dostavka : Доставка', 'cf_noty_serdtsa : Ноты сердца', 'cf_god : Год', 'cf_obem : Объем',
              'cf_bazovye_noty : Базовые ноты', 'yml_model : Модель',
              'yml_delivery_options_enabled : Параметры курьерской доставки по своему региону',
              'yml_delivery_options_cost : Стоимость доставки для своего региона']

DESCRIPTION = """<p style="
    text-align: center;
"><span style="display: inline-block;width: 320px;text-align: center;vertical-align: top;padding: 6px;margin: 0 0 20px;border: 1px solid #f5f5f5;"><strong>Ассортимент</strong><br />
<span style="
    font-size: 14px;
">модные новинки и изысканные ароматы</span></span> <span style="display: inline-block;min-width: 10px;"> </span> <span style="display: inline-block;width: 320px;text-align: center;vertical-align: top;margin: 0 0 20px;padding: 6px;border: 1px solid #f5f5f5;"><strong> 100% гарантия</strong><br />
<span style="
    font-size: 14px;
">вся продукция от мировых брендов</span></span> <span style="display: inline-block;min-width: 10px;"> </span> <span style="display: inline-block;width: 320px;text-align: center;vertical-align: top;margin: 0 0 20px;padding: 6px;border: 1px solid #f5f5f5;"><strong> Доставка</strong><br />
<span style="
    font-size: 14px;
">быстрая доставка по всей России</span></span> <span style="display: inline-block;min-width: 12px;"> </span></p>
"""

CLASSIFICATIONS = ['одеколон', 'туалетная вода', 'парфюмерная вода', 'духи', 'мыло']
CATEGORIES = {
    'жен': 'Для женщин',
    'муж': 'Для мужчин',
    'унисекс': 'Унисекс',
}

if os.path.isfile(BRENDS_FILE):
    with open(BRENDS_FILE, 'r', encoding='utf-8') as json_file:
        BRENDS = json.load(json_file)
else:
    BRENDS = perfume_parser.get_brends()
    perfume_parser.save_json(BRENDS, BRENDS_FILE)


def write_header(file_name=CSV_FILE):
    with open(file_name, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(CSV_HEADER)


def save_data(data, file_name=CSV_FILE, encoding='utf-8'):
    with open(file_name, "a", newline='', encoding=encoding) as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerows(data)


def load_data(file_name=CSV_FILE):
    with open(file_name, "r", newline='', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        data = [el for el in reader]
        return data


def _parse_brend(text):
    brend = None
    for BREND in BRENDS:
        if BREND.lower() in text.lower():
            brend = BREND
            break
    return brend


def _parse_classification(text):
    classification = None
    for CLASSIFICATION in CLASSIFICATIONS:
        if CLASSIFICATION in text.lower():
            classification = CLASSIFICATION
            break
    return classification


def _parse_category(text):
    if 'муж' in text:
        finish_category = CATEGORIES['муж']
        return finish_category
    elif 'жен' in text:
        finish_category = CATEGORIES['жен']
        return finish_category
    elif 'унисекс' in text:
        finish_category = CATEGORIES['унисекс']
        return finish_category
    elif 'тушь' in text:
        finish_category = CATEGORIES['жен']
        return finish_category
    else:
        finish_category = CATEGORIES['жен']
        return finish_category


def _parse_volume(text):
    volume_search = re.search('(\S+)ml', text)
    if volume_search:
        return '{}ml'.format(volume_search.group(1))
    elif re.search('(\S+)гр\.', text):
        volume = '{}гр.'.format(re.search('(\S+)гр\.', text).group(1))
        return volume
    elif re.search('(\S+)M ', text):
        volume = '{}M'.format(re.search('(\S+)M ', text).group(1))
        return volume
    elif re.search('(\S+)G ', text):
        volume = '{}G'.format(re.search('(\S+)G ', text).group(1))
        return volume
    else:
        return ''


def _get_perfume_data_from_row(row):
    cols_auto = row.select('.col-auto')
    cols = row.select('.col')
    article = cols_auto[0].text
    all_text = cols[0].text
    print(all_text)
    brend = _parse_brend(all_text)
    if brend:
        text_without_brend = all_text.split(brend, maxsplit=1)[-1].strip()
    else:
        return
    category = _parse_category(text_without_brend)
    name = text_without_brend.split('(')[0].strip()
    if not name:
        name = brend
    volume = _parse_volume(text_without_brend)
    classification = _parse_classification(text_without_brend)
    price = cols_auto[1].text.strip()
    if u'\xa0' in price:
        price = price.replace(u'\xa0', '')
    if '.' in price:
        price = price.replace('.', ',')
    perfume_data = [text_without_brend, brend, None, 3, article, category, None, 'mode', '', DESCRIPTION, 1000, 0, 0,
                    'шт.', 0.5, 'kg', 0, 0, 1, 0, 0, price, 0, 'RUB', 0, name, name, name, name, None, None, None,
                    '', classification, 'Быстрая доставка по всей России', '', '', volume, '', None,
                    0, None]
    return perfume_data


def _parse_max_page(soup):
    return int(soup.select_one('.bx-pagination-container').select('li')[-2].text)


def parsing(start_page=None):
    if not start_page:
        write_header()
        page = 1
    else:
        page = start_page
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')
    max_page = _parse_max_page(soup)
    uniq_names = []
    while page != max_page + 1:
        print('Страница {}'.format(page))
        perfumes_data = []
        if page != 1:
            url = 'https://optparf.ru/?page=page-{}'.format(page)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'lxml')
        rows = soup.select('.row.table-body')
        for row in rows:
            perfume_data = _get_perfume_data_from_row(row)
            if perfume_data:
                mode = None
                uniq_name = '{} {} {}'.format(perfume_data[25], perfume_data[1], perfume_data[5])
                if uniq_name in uniq_names:
                    mode = '*'
                else:
                    uniq_names.append(uniq_name)
                perfume_data[7] = mode
                perfumes_data.append(perfume_data)
        save_data(perfumes_data)
        page += 1
    print('ЗАВЕРШЕНО')


if __name__ == '__main__':
    parsing()
