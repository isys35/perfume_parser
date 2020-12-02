import requests
from bs4 import BeautifulSoup
import json

CATEGORIES_URLS = [
    'https://духи.рф/catalog/women',
    'https://духи.рф/catalog/men'
]


def save_page(response_str, file_name='page.html'):
    with open(file_name, 'w', encoding='utf8') as html_file:
        html_file.write(response_str)


def save_json(data, file_name='data.json'):
    with open(file_name, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=True)


def get_brends():
    brends = []
    for url in CATEGORIES_URLS:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        for brend_block in soup.select('a.wrap_a.items.type_name'):
            print(brend_block.text)
            if brend_block.text not in brends:
                brends.append(brend_block.text)
    return brends


if __name__ == '__main__':
    brends = get_brends()
    save_json(brends, 'brends.json')
