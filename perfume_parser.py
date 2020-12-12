import requests
from bs4 import BeautifulSoup
import json

CATEGORIES_URLS = [
    'https://духи.рф/catalog/women',
    'https://духи.рф/catalog/men'
]


def save_page(response_str, file_name='page.html'):
    with open(file_name, 'w', encoding='utf-8') as html_file:
        html_file.write(response_str)


def save_json(data, file_name='data.json'):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=True)


def get_brends():
    brends = []
    for url in CATEGORIES_URLS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        for brend_block in soup.select('a.wrap_a.items.type_name'):
            if brend_block.text not in brends and brend_block.text != 'Gerani':
                brends.append(brend_block.text)
    return brends


def resorted_brends():
    with open('brends.json', 'r', encoding='utf-8') as json_file:
        brends = json.load(json_file)
    brends.sort(key=len, reverse=True)
    save_json(brends, 'brends2.json')



if __name__ == '__main__':
    resorted_brends()
