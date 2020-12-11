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

    data[581][9] = optfarm_parser.DESCRIPTION
    data[581][1] = 'Alexander McQueen'
    data[581][0] = 'Blazing Lily (женские) 75ml парфюмерная вода'
    data[581][25] = 'Blazing Lily'
    data[581][26] = 'Blazing Lily'
    data[581][27] = 'Blazing Lily'
    data[581][28] = 'Blazing Lily'

    data[582][9] = optfarm_parser.DESCRIPTION
    data[582][1] = 'Alexander McQueen'
    data[582][0] = 'Blazing Lily (женские) 75ml парфюмерная вода *Тестер'
    data[582][25] = 'Blazing Lily'
    data[582][26] = 'Blazing Lily'
    data[582][27] = 'Blazing Lily'
    data[582][28] = 'Blazing Lily'

    data[1833][9] = optfarm_parser.DESCRIPTION
    data[1833][1] = 'Baldinini'
    data[1833][0] = 'Baldinini (женские) 40ml парфюмерная вода *Tester'
    data[1833][25] = ''
    data[1833][26] = ''
    data[1833][27] = ''
    data[1833][28] = ''

    data[1834][9] = optfarm_parser.DESCRIPTION
    data[1834][1] = 'Baldinini'
    data[1834][0] = 'Baldinini (женские) 75ml парфюмерная вода'
    data[1834][25] = ''
    data[1834][26] = ''
    data[1834][27] = ''
    data[1834][28] = ''

    data[1835][9] = optfarm_parser.DESCRIPTION
    data[1835][1] = 'Baldinini'
    data[1835][0] = 'Baldinini (женские) 75ml парфюмерная вода *Tester'
    data[1835][25] = ''
    data[1835][26] = ''
    data[1835][27] = ''
    data[1835][28] = ''

    data[1836][9] = optfarm_parser.DESCRIPTION
    data[1836][1] = 'Baldinini'
    data[1836][0] = 'Gimmy (мужские) 100ml туалетная вода'
    data[1836][25] = 'Gimmy'
    data[1836][26] = 'Gimmy'
    data[1836][27] = 'Gimmy'
    data[1836][28] = 'Gimmy'

    data[1837][9] = optfarm_parser.DESCRIPTION
    data[1837][1] = 'Baldinini'
    data[1837][0] = 'Parfum Glace (женские) 75ml парфюмерная вода'
    data[1837][25] = 'Parfum Glace'
    data[1837][26] = 'Parfum Glace'
    data[1837][27] = 'Parfum Glace'
    data[1837][28] = 'Parfum Glace'

    data[1838][9] = optfarm_parser.DESCRIPTION
    data[1838][1] = 'Baldinini'
    data[1838][0] = 'Parfum Glace (женские) 75ml парфюмерная вода *Tester'
    data[1838][25] = 'Parfum Glace'
    data[1838][26] = 'Parfum Glace'
    data[1838][27] = 'Parfum Glace'
    data[1838][28] = 'Parfum Glace'

    data[2010][9] = optfarm_parser.DESCRIPTION
    data[2010][1] = 'Beverly Hills Giorgio'
    data[2010][0] = 'Aire (женские) 90ml туалетная вода'
    data[2010][25] = 'Aire'
    data[2010][26] = 'Aire'
    data[2010][27] = 'Aire'
    data[2010][28] = 'Aire'

    data[3922][9] = optfarm_parser.DESCRIPTION
    data[3922][1] = 'Celine Dion'
    data[3922][0] = 'Belong (женские) 100ml туалетная вода *Tester'
    data[3922][25] = 'Belong'
    data[3922][26] = 'Belong'
    data[3922][27] = 'Belong'
    data[3922][28] = 'Belong'

    data[3923][9] = optfarm_parser.DESCRIPTION
    data[3923][1] = 'Celine Dion'
    data[3923][0] = 'Chic (женские) 100ml туалетная вода *Tester'
    data[3923][25] = 'Chic'
    data[3923][26] = 'Chic'
    data[3923][27] = 'Chic'
    data[3923][28] = 'Chic'

    data[3924][9] = optfarm_parser.DESCRIPTION
    data[3924][1] = 'Celine Dion'
    data[3924][0] = 'Parfum Notes (женские) 100ml туалетная вода *Tester'
    data[3924][25] = 'Parfum Notes'
    data[3924][26] = 'Parfum Notes'
    data[3924][27] = 'Parfum Notes'
    data[3924][28] = 'Parfum Notes'

    data[5093][9] = optfarm_parser.DESCRIPTION
    data[5093][1] = 'Comme des Garcons'
    data[5093][0] = 'Andy Warhol`s You`re In (унисекс) 100ml туалетная вода *Тестер'
    data[5093][25] = 'Andy Warhol`s You`re In'
    data[5093][26] = 'Andy Warhol`s You`re In'
    data[5093][27] = 'Andy Warhol`s You`re In'
    data[5093][28] = 'Andy Warhol`s You`re In'
    for i in range(5096, 5108):
        # data[i][0] = 'Comptoir Sud Pacifique ' + data[i][0]
        data[i][1] = 'Comptoir Sud Pacifique'

    for i in range(5109, 5172):
        # data[i][0] = 'Comptoir Sud Pacifique ' + data[i][0]
        data[i][1] = 'Comptoir Sud Pacifique'

    for i in range(5173, 5208):
        # data[i][0] = 'Comptoir Sud Pacifique ' + data[i][0]
        data[i][1] = 'Comptoir Sud Pacifique'

    data[5108][9] = optfarm_parser.DESCRIPTION
    data[5108][1] = 'Comptoir Sud Pacifique'
    data[5108][0] = 'Barbier Des Isles (мужские) 100ml туалетная вода'
    data[5108][25] = 'Barbier Des Isles'
    data[5108][26] = 'Barbier Des Isles'
    data[5108][27] = 'Barbier Des Isles'
    data[5108][28] = 'Barbier Des Isles'

    data[5172][9] = optfarm_parser.DESCRIPTION
    data[5172][1] = 'Comptoir Sud Pacifique'
    data[5172][0] = 'Princesse Muscat (женские) 100ml туалетная вода'
    data[5172][25] = 'Princesse Muscat'
    data[5172][26] = 'Princesse Muscat'
    data[5172][27] = 'Princesse Muscat'
    data[5172][28] = 'Princesse Muscat'

    data[5992][9] = optfarm_parser.DESCRIPTION
    data[5992][1] = 'Dolce & Gabbana'
    data[5992][0] = 'Velvet Desert Oud (унисекс) 50ml парфюмерная вода'
    data[5992][25] = 'Velvet Desert Oud'
    data[5992][26] = 'Velvet Desert Oud'
    data[5992][27] = 'Velvet Desert Oud'
    data[5992][28] = 'Velvet Desert Oud'

    data[5993][9] = optfarm_parser.DESCRIPTION
    data[5993][1] = 'Dolce & Gabbana'
    data[5993][0] = 'Velvet Desert Oud (унисекс) 50ml парфюмерная вода *Тестер'
    data[5993][25] = 'Velvet Desert Oud'
    data[5993][26] = 'Velvet Desert Oud'
    data[5993][27] = 'Velvet Desert Oud'
    data[5993][28] = 'Velvet Desert Oud'

    for i in range(6615, 6639):
        data[i][0] = data[i][0].replace('Parfums ', '')
        data[i][1] = 'Ella K Parfums'
        data[i][25] = data[i][25].replace('Parfums ', '')
        data[i][26] = data[i][26].replace('Parfums ', '')
        data[i][27] = data[i][27].replace('Parfums ', '')
        data[i][28] = data[i][28].replace('Parfums ', '')

    data[7201][9] = optfarm_parser.DESCRIPTION
    data[7201][1] = 'Evody Parfums'
    data[7201][0] = 'Desert Nocturne (унисекс) 30ml духи'
    data[7201][25] = 'Desert Nocturne'
    data[7201][26] = 'Desert Nocturne'
    data[7201][27] = 'Desert Nocturne'
    data[7201][28] = 'Desert Nocturne'

    data[8718][9] = optfarm_parser.DESCRIPTION
    data[8718][1] = 'Givenchy'
    data[8718][0] = 'Very Irresistible Fresh Attitude (мужские) 100ml туалетная вода'
    data[8718][25] = 'Very Irresistible Fresh Attitude'
    data[8718][26] = 'Very Irresistible Fresh Attitude'
    data[8718][27] = 'Very Irresistible Fresh Attitude'
    data[8718][28] = 'Very Irresistible Fresh Attitude'

    data[8719][9] = optfarm_parser.DESCRIPTION
    data[8719][1] = 'Givenchy'
    data[8719][0] = 'Very Irresistible Fresh Attitude (мужские) 100ml туалетная вода *Tester'
    data[8719][25] = 'Very Irresistible Fresh Attitude'
    data[8719][26] = 'Very Irresistible Fresh Attitude'
    data[8719][27] = 'Very Irresistible Fresh Attitude'
    data[8719][28] = 'Very Irresistible Fresh Attitude'

    data[8720][9] = optfarm_parser.DESCRIPTION
    data[8720][1] = 'Givenchy'
    data[8720][0] = 'Very Irresistible Fresh Attitude Summer Cocktail (мужские) 100ml туалетная вода'
    data[8720][25] = 'Very Irresistible Fresh Attitude Summer Cocktail'
    data[8720][26] = 'Very Irresistible Fresh Attitude Summer Cocktail'
    data[8720][27] = 'Very Irresistible Fresh Attitude Summer Cocktail'
    data[8720][28] = 'Very Irresistible Fresh Attitude Summer Cocktail'

    data[8759][9] = optfarm_parser.DESCRIPTION
    data[8759][1] = 'Goldfield & Banks Australia'
    data[8759][0] = 'Desert Rosewood (унисекс) 100ml парфюмерная вода'
    data[8759][25] = 'Desert Rosewood'
    data[8759][26] = 'Desert Rosewood'
    data[8759][27] = 'Desert Rosewood'
    data[8759][28] = 'Desert Rosewood'

    data[8760][9] = optfarm_parser.DESCRIPTION
    data[8760][1] = 'Goldfield & Banks Australia'
    data[8760][0] = 'Desert Rosewood (унисекс) 100ml парфюмерная вода *Тестер'
    data[8760][25] = 'Desert Rosewood'
    data[8760][26] = 'Desert Rosewood'
    data[8760][27] = 'Desert Rosewood'
    data[8760][28] = 'Desert Rosewood'

    data[9808][0] = 'Equipage Geranium (мужские) 100ml туалетная вода *Тестер'

    data[10474][9] = optfarm_parser.DESCRIPTION
    data[10474][1] = 'Illuminum'
    data[10474][0] = 'Hindi OUD (унисекс) 100ml парфюмерная вода'
    data[10474][25] = 'Hindi OUD'
    data[10474][26] = 'Hindi OUD'
    data[10474][27] = 'Hindi OUD'
    data[10474][28] = 'Hindi OUD'

    data[12152][9] = optfarm_parser.DESCRIPTION
    data[12152][1] = 'Kenzo'
    data[12152][0] = 'Kenzo Homme Fresh Eau de Parfum (мужские) 100ml парфюмерная вода'
    data[12152][25] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12152][26] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12152][27] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12152][28] = 'Kenzo Homme Fresh Eau de Parfum'

    data[12153][9] = optfarm_parser.DESCRIPTION
    data[12153][1] = 'Kenzo'
    data[12153][0] = 'Kenzo Homme Fresh Eau de Parfum (мужские) 100ml парфюмерная вода *Тестер'
    data[12153][25] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12153][26] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12153][27] = 'Kenzo Homme Fresh Eau de Parfum'
    data[12153][28] = 'Kenzo Homme Fresh Eau de Parfum'

    data[12433][9] = optfarm_parser.DESCRIPTION
    data[12433][1] = 'Kilian'
    data[12433][0] = 'Love the way you Feel (унисекс) 50ml парфюмерная вода'
    data[12433][25] = 'Love the way you Feel'
    data[12433][26] = 'Love the way you Feel'
    data[12433][27] = 'Love the way you Feel'
    data[12433][28] = 'Love the way you Feel'

    data[12434][9] = optfarm_parser.DESCRIPTION
    data[12434][1] = 'Kilian'
    data[12434][0] = 'Love the way you Feel (унисекс) 50ml парфюмерная вода *Тестер'
    data[12434][25] = 'Love the way you Feel'
    data[12434][26] = 'Love the way you Feel'
    data[12434][27] = 'Love the way you Feel'
    data[12434][28] = 'Love the way you Feel'

    data[12684][9] = optfarm_parser.DESCRIPTION
    data[12684][1] = 'La Maison de la Vanille'
    data[12684][0] = 'Vanille Divine des Tropiques (женские) 1.5ml туалетная вода *Пробник'
    data[12684][25] = 'Vanille Divine des Tropiques'
    data[12684][26] = 'Vanille Divine des Tropiques'
    data[12684][27] = 'Vanille Divine des Tropiques'
    data[12684][28] = 'Vanille Divine des Tropiques'

    data[12685][9] = optfarm_parser.DESCRIPTION
    data[12685][1] = 'La Maison de la Vanille'
    data[12685][0] = 'Vanille Divine des Tropiques (женские) 100ml парфюмерная вода'
    data[12685][25] = 'Vanille Divine des Tropiques'
    data[12685][26] = 'Vanille Divine des Tropiques'
    data[12685][27] = 'Vanille Divine des Tropiques'
    data[12685][28] = 'Vanille Divine des Tropiques'

    data[12686][9] = optfarm_parser.DESCRIPTION
    data[12686][1] = 'La Maison de la Vanille'
    data[12686][0] = 'Vanille Divine des Tropiques (женские) 30ml парфюмерная вода'
    data[12686][25] = 'Vanille Divine des Tropiques'
    data[12686][26] = 'Vanille Divine des Tropiques'
    data[12686][27] = 'Vanille Divine des Tropiques'
    data[12686][28] = 'Vanille Divine des Tropiques'

    data[13640][9] = optfarm_parser.DESCRIPTION
    data[13640][1] = 'Linari'
    data[13640][0] = 'Porta del Cielo (унисекс) 100ml парфюмерная вода'
    data[13640][25] = 'Porta del Cielo'
    data[13640][26] = 'Porta del Cielo'
    data[13640][27] = 'Porta del Cielo'
    data[13640][28] = 'Porta del Cielo'

    data[13641][9] = optfarm_parser.DESCRIPTION
    data[13641][1] = 'Linari'
    data[13641][0] = 'Porta del Cielo (унисекс) 100ml парфюмерная вода *Тестер'
    data[13641][25] = 'Porta del Cielo'
    data[13641][26] = 'Porta del Cielo'
    data[13641][27] = 'Porta del Cielo'
    data[13641][28] = 'Porta del Cielo'

    data[14416][9] = optfarm_parser.DESCRIPTION
    data[14416][1] = 'Maitre Parfumeur et Gantier'
    data[14416][0] = 'Ambre Precieux (мужские) 120ml парфюмерная вода'
    data[14416][25] = 'Ambre Precieux'
    data[14416][26] = 'Ambre Precieux'
    data[14416][27] = 'Ambre Precieux'
    data[14416][28] = 'Ambre Precieux'

    data[14417][9] = optfarm_parser.DESCRIPTION
    data[14417][1] = 'Maitre Parfumeur et Gantier'
    data[14417][0] = 'Bahiana (женские) 100ml туалетная вода'
    data[14417][25] = 'Bahiana'
    data[14417][26] = 'Bahiana'
    data[14417][27] = 'Bahiana'
    data[14417][28] = 'Bahiana'

    data[14418][9] = optfarm_parser.DESCRIPTION
    data[14418][1] = 'Maitre Parfumeur et Gantier'
    data[14418][0] = 'Fraicheur Muskissime Extravagante (женские) 100ml парфюмерная вода'
    data[14418][25] = 'Fraicheur Muskissime Extravagante'
    data[14418][26] = 'Fraicheur Muskissime Extravagante'
    data[14418][27] = 'Fraicheur Muskissime Extravagante'
    data[14418][28] = 'Fraicheur Muskissime Extravagante'

    data[14558][9] = optfarm_parser.DESCRIPTION
    data[14558][1] = 'Mancera'
    data[14558][0] = 'Hindu Kush (унисекс) 120ml парфюмерная вода'
    data[14558][25] = 'Hindu Kush'
    data[14558][26] = 'Hindu Kush'
    data[14558][27] = 'Hindu Kush'
    data[14558][28] = 'Hindu Kush'

    data[14559][9] = optfarm_parser.DESCRIPTION
    data[14559][1] = 'Mancera'
    data[14559][0] = 'Hindu Kush (унисекс) 120ml парфюмерная вода *Тестер'
    data[14559][25] = 'Hindu Kush'
    data[14559][26] = 'Hindu Kush'
    data[14559][27] = 'Hindu Kush'
    data[14559][28] = 'Hindu Kush'

    data[14560][9] = optfarm_parser.DESCRIPTION
    data[14560][1] = 'Mancera'
    data[14560][0] = 'Hindu Kush (унисекс) 2ml парфюмерная вода *Пробник'
    data[14560][25] = 'Hindu Kush'
    data[14560][26] = 'Hindu Kush'
    data[14560][27] = 'Hindu Kush'
    data[14560][28] = 'Hindu Kush'

    data[14561][9] = optfarm_parser.DESCRIPTION
    data[14561][1] = 'Mancera'
    data[14561][0] = 'Hindu Kush (унисекс) 8ml парфюмерная вода'
    data[14561][25] = 'Hindu Kush'
    data[14561][26] = 'Hindu Kush'
    data[14561][27] = 'Hindu Kush'
    data[14561][28] = 'Hindu Kush'

    data[14772][9] = optfarm_parser.DESCRIPTION
    data[14772][1] = 'Marc Jacobs'
    data[14772][0] = 'Daisy Eau So Fresh Daze (женские) 75ml туалетная вода'
    data[14772][25] = 'Daisy Eau So Fresh Daze'
    data[14772][26] = 'Daisy Eau So Fresh Daze'
    data[14772][27] = 'Daisy Eau So Fresh Daze'
    data[14772][28] = 'Daisy Eau So Fresh Daze'

    data[14773][9] = optfarm_parser.DESCRIPTION
    data[14773][1] = 'Marc Jacobs'
    data[14773][0] = 'Daisy Eau So Fresh Kiss (женские) 75ml туалетная вода *Тестер'
    data[14773][25] = 'Daisy Eau So Fresh Kiss'
    data[14773][26] = 'Daisy Eau So Fresh Kiss'
    data[14773][27] = 'Daisy Eau So Fresh Kiss'
    data[14773][28] = 'Daisy Eau So Fresh Kiss'

    data[14774][9] = optfarm_parser.DESCRIPTION
    data[14774][1] = 'Marc Jacobs'
    data[14774][0] = 'Daisy Eau So Fresh Sunshine (женские) 75ml туалетная вода *Тестер'
    data[14774][25] = 'Daisy Eau So Fresh Sunshine'
    data[14774][26] = 'Daisy Eau So Fresh Sunshine'
    data[14774][27] = 'Daisy Eau So Fresh Sunshine'
    data[14774][28] = 'Daisy Eau So Fresh Sunshine'

    data[14775][9] = optfarm_parser.DESCRIPTION
    data[14775][1] = 'Marc Jacobs'
    data[14775][0] = 'Daisy Eau So Fresh Sunshine (женские) 75ml туалетная вода'
    data[14775][25] = 'Daisy Eau So Fresh Sunshine'
    data[14775][26] = 'Daisy Eau So Fresh Sunshine'
    data[14775][27] = 'Daisy Eau So Fresh Sunshine'
    data[14775][28] = 'Daisy Eau So Fresh Sunshine'

    data[14776][9] = optfarm_parser.DESCRIPTION
    data[14776][1] = 'Marc Jacobs'
    data[14776][0] = 'Daisy Eau So Fresh Twinkle (женские) 75ml туалетная вода *Тестер'
    data[14776][25] = 'Daisy Eau So Fresh Twinkle'
    data[14776][26] = 'Daisy Eau So Fresh Twinkle'
    data[14776][27] = 'Daisy Eau So Fresh Twinkle'
    data[14776][28] = 'Daisy Eau So Fresh Twinkle'

    data[14791][9] = optfarm_parser.DESCRIPTION
    data[14791][1] = 'Marc Jacobs'
    data[14791][0] = 'Divine Decadence (женские) 100ml парфюмерная вода'
    data[14791][25] = 'Divine Decadence'
    data[14791][26] = 'Divine Decadence'
    data[14791][27] = 'Divine Decadence'
    data[14791][28] = 'Divine Decadence'

    data[14792][9] = optfarm_parser.DESCRIPTION
    data[14792][1] = 'Marc Jacobs'
    data[14792][0] = 'Divine Decadence (женские) 100ml парфюмерная вода *Тестер'
    data[14792][25] = 'Divine Decadence'
    data[14792][26] = 'Divine Decadence'
    data[14792][27] = 'Divine Decadence'
    data[14792][28] = 'Divine Decadence'

    data[14793][9] = optfarm_parser.DESCRIPTION
    data[14793][1] = 'Marc Jacobs'
    data[14793][0] = 'Divine Decadence (женские) 30ml парфюмерная вода'
    data[14793][25] = 'Divine Decadence'
    data[14793][26] = 'Divine Decadence'
    data[14793][27] = 'Divine Decadence'
    data[14793][28] = 'Divine Decadence'

    data[14794][9] = optfarm_parser.DESCRIPTION
    data[14794][1] = 'Marc Jacobs'
    data[14794][0] = 'Divine Decadence (женские) 50ml парфюмерная вода'
    data[14794][25] = 'Divine Decadence'
    data[14794][26] = 'Divine Decadence'
    data[14794][27] = 'Divine Decadence'
    data[14794][28] = 'Divine Decadence'

    data[14795][9] = optfarm_parser.DESCRIPTION
    data[14795][1] = 'Marc Jacobs'
    data[14795][0] = 'Divine Decadence (женские) 50ml парфюмерная вода *Тестер'
    data[14795][25] = 'Divine Decadence'
    data[14795][26] = 'Divine Decadence'
    data[14795][27] = 'Divine Decadence'
    data[14795][28] = 'Divine Decadence'

    data[14823][9] = optfarm_parser.DESCRIPTION
    data[14823][1] = 'Marc O`Polo'
    data[14823][0] = 'Signature for woman (женские) 15ml туалетная вода'
    data[14823][25] = 'Signature for woman'
    data[14823][26] = 'Signature for woman'
    data[14823][27] = 'Signature for woman'
    data[14823][28] = 'Signature for woman'

    data[14824][9] = optfarm_parser.DESCRIPTION
    data[14824][1] = 'Marc O`Polo'
    data[14824][0] = 'Signature for woman (женские) 50ml туалетная вода'
    data[14824][25] = 'Signature for woman'
    data[14824][26] = 'Signature for woman'
    data[14824][27] = 'Signature for woman'
    data[14824][28] = 'Signature for woman'

    data[14908][9] = optfarm_parser.DESCRIPTION
    data[14908][1] = 'Marina de Bourbon'
    data[14908][0] = 'Royal Marina Rubis Princesse (женские) 100ml парфюмерная вода *Tester'
    data[14908][25] = 'Royal Marina Rubis Princesse'
    data[14908][26] = 'Royal Marina Rubis Princesse'
    data[14908][27] = 'Royal Marina Rubis Princesse'
    data[14908][28] = 'Royal Marina Rubis Princesse'

    data[14909][9] = optfarm_parser.DESCRIPTION
    data[14909][1] = 'Marina de Bourbon'
    data[14909][0] = 'Royal Marina Rubis Princesse (женские) 30ml парфюмерная вода'
    data[14909][25] = 'Royal Marina Rubis Princesse'
    data[14909][26] = 'Royal Marina Rubis Princesse'
    data[14909][27] = 'Royal Marina Rubis Princesse'
    data[14909][28] = 'Royal Marina Rubis Princesse'

    data[14910][9] = optfarm_parser.DESCRIPTION
    data[14910][1] = 'Marina de Bourbon'
    data[14910][0] = 'Royal Marina Rubis Princesse (женские) 50ml парфюмерная вода'
    data[14910][25] = 'Royal Marina Rubis Princesse'
    data[14910][26] = 'Royal Marina Rubis Princesse'
    data[14910][27] = 'Royal Marina Rubis Princesse'
    data[14910][28] = 'Royal Marina Rubis Princesse'

    data[14911][9] = optfarm_parser.DESCRIPTION
    data[14911][1] = 'Marina de Bourbon'
    data[14911][0] = 'Royal Marina Rubis Princesse (женские) 3,5ml парфюмерная вода *Mini'
    data[14911][25] = 'Royal Marina Rubis Princesse'
    data[14911][26] = 'Royal Marina Rubis Princesse'
    data[14911][27] = 'Royal Marina Rubis Princesse'
    data[14911][28] = 'Royal Marina Rubis Princesse'



    optfarm_parser.save_data(data, 'data2.csv')


if __name__ == '__main__':
    updater()
