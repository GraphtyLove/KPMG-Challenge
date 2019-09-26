# * ---------- Imports ---------- *
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re


# * ---------- Scrap meta-data ---------- *
# All the functions that we can call in the pre-processing and scraping and return a Json object
def scrap_meta_data(entreprise_number):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }
    # Json that contain the meta-data
    json_formated = {}
    json_key = ''
    # URL where where we will scrap meta-data
    url = f'https://kbopub.economie.fgov.be/kbopub/toonondernemingps.html?ondernemingsnummer={entreprise_number}&lang=fr'
    
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')
    
    tr = soup.select('tr')

    title_two_row_formated_data = ['Généralités', 'Données financières',
                                   'In general', 'Financial information',
                                   'Algemeen', 'Financiële gegevens']
    
    title_three_formated_data = ['Fonctions', 'Functions', 'Functies']

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
                        json_formated[json_title_key] = {}
                except:
                    continue

                if json_title_key in title_two_row_formated_data:
                    if len(td_content) > 0:
                        if td_text == 'Pas de données reprises dans la BCE.':
                            td_text = "None"

                        if td_content == full_data[0]:
                            json_key = td_text
                        else:
                            if json_key == "Numéro d'entreprise:":
                                json_formated["business_number"] = td_text.replace('.', '')
                            else:
                                json_formated[json_title_key][json_key] = td_text.replace('Dénomination', ' Dénomination')

                elif json_title_key in title_three_formated_data:
                    json_formated[json_title_key] = {
                        td_text: {'nom': next(iter_job).get_text().strip().replace('   ', ' ').replace(' ,', ''),
                                  'date': next(iter_job).get_text().strip().replace('	', '')
                                  }
                    }
                else:
                    json_formated[json_title_key] = td_text.replace('Depuis', ' Depuis')

            except StopIteration:
                break

        # Get all <td> with the class 'tdata2' (the list of the entreprises)
        td_tdata2 = soup.find_all('td', {'class': 'tdata2'})

        for k, v in enumerate(td_tdata2):
            # Select informations
            company_account_number = re.findall('BE[0-9]{4}\.[0-9]{3}\.[0-9]{3}', v.get_text())[0]
            json_formated['bank_account'] = company_account_number


    return json_formated


# * ---------- Get business number from company name ---------- *
# Scrap staatsbladmonitor.be to get name + business number + bank account from string input value.
# Return a Json with a name and a business number
def business_number_from_name(input_name_string):
    output_json = {}

    input_name_string = input_name_string.replace(' ', '+')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }

    # Scraping
    url = f'https://www.staatsbladmonitor.be/onderneming-zoeken.html?search={input_name_string}'
    req = Request(url=url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'lxml')

    # Get all <td> with the class 'tdata2' (the list of the entreprises)
    td_tdata2 = soup.find_all('td', {'class': 'tdata2'})

    for k, v in enumerate(td_tdata2):
        # Select informations
        company_name = v.find('b').get_text()
        company_business_number = re.findall('[0-9]{10}', v.find('a')['href'])[0]
        company_account_number = re.findall('BE[0-9]{4}\.[0-9]{3}\.[0-9]{3}', v.get_text())[0]

        # Store data in a json format
        output_json[k] = {}
        output_json[k]['companyName'] = company_name
        output_json[k]['businessNumber'] = company_business_number
        output_json[k]['account number'] = company_account_number

    return output_json