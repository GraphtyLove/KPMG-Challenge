import json
import time
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

YEARS = [2014, 2015, 2016, 2018, 2019]
for YEAR in YEARS:
    print(f'* ---------- START: {YEAR} ---------- *')
    loaded_json = {}
    with open(f'../assets/json/links_entreprises/links_entreprises_{YEAR}.json', 'r', encoding='utf-8') as file:
        file = file.read()
        loaded_json = json.loads(file)

    for link in loaded_json:
        json_meta_data = {}
        entreprise_number = re.findall('[0-9]{10}', link)[0]
        Json_formated = {}
        json_key = ''
        try:
            # Scraping
            url = f'https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer={entreprise_number}&lang=fr'
            time.sleep(0.2)
            req = Request(url=url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')
            tr = soup.select('tr')

            title_two_row_formated_data = ['Généralités', 'Données financières',
                                           'In general', 'Financial information',
                                           'Algemeen', 'Financiële gegevens']

            title_two_three_formated_data = ['Fonctions', 'Functions', 'Functies']

            function_count = 0

            for tr_content in tr:
                full_data = tr_content.find_all('td')
                iter_job = iter(full_data)
                while True:
                    try:
                        td_content = next(iter_job)
                        td_text = td_content.get_text().strip()
                        td_text = td_text.replace('	', '')
                        try:
                            if 'I' in td_content['class']:
                                json_title_key = td_text
                                Json_formated[json_title_key] = {}


                        except:
                            continue

                        if json_title_key in title_two_row_formated_data:
                            if len(td_content) > 0:
                                if td_text == 'Pas de données reprises dans la BCE.':
                                    td_text = None

                                if td_content == full_data[0]:
                                    json_key = td_text
                                else:
                                    Json_formated[json_title_key][json_key] = td_text

                        elif json_title_key in title_two_three_formated_data:
                            Json_formated[json_title_key] = {
                                td_text: {'nom': next(iter_job).get_text().strip().replace('   ', ' ').replace(' ,', ''),
                                          'date': next(iter_job).get_text().strip().replace('	', '')
                                          }
                            }
                        else:
                            Json_formated[json_title_key] = td_text.replace('Depuis', ' Depuis')
                    except StopIteration:
                        break

            with open(f'../assets/json/meta-data/{YEAR}/{entreprise_number}.meta.json', 'w', encoding='utf-8') as file:
                json.dump(Json_formated, file, ensure_ascii=False, indent=4)
            print(f'* --- {YEAR}: Meta-data of entreprise: {entreprise_number} => OK --- *')
        except:
            print(f"!!! --- {YEAR}: Error with entreprise: {entreprise_number} --- !!!")
