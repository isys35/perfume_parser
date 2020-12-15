import requests
import sys

CLIENT_ID = "k5dX16WlfEArklA1R8FW"
SECRET_KEY = 'RT9dd5P4FK7QsuFSnEmLKATLovpH5jMgeFB'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Authorization': 'TOKEN {}'.format(CLIENT_ID)
}
POST_URL = 'https://api.imageban.ru/v1'


def load_image_and_get_url(url):
    json_data = {
        'secret_key': SECRET_KEY,
        'url': url,
    }
    response = requests.post(POST_URL, json_data, headers=HEADERS)
    try:
        final_url = response.json()['data']['link']
    except KeyError:
        print(response.text)
        sys.exit()
    return final_url


if __name__ == '__main__':
    load_image_and_get_url('https://cdn2.randewoo.ru/img/204649/z/1')
