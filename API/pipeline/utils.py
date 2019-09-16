# * ---------- Imports ---------- *
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import pytesseract
from PIL import Image
from wand.image import Image as Img
import os
import spacy
from spacy_langdetect import LanguageDetector
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
    
    title_two_three_formated_data = ['Fonctions', 'Functions', 'Functies']

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
                            td_text = None

                        if td_content == full_data[0]:
                            json_key = td_text
                        else:
                            json_formated[json_title_key][json_key] = td_text

                elif json_title_key in title_two_three_formated_data:
                    print(json_title_key)
                    json_formated[json_title_key] = {
                        td_text: {'nom': next(iter_job).get_text().strip().replace('   ', ' ').replace(' ,', ''),
                                  'date': next(iter_job).get_text().strip().replace('	', '')
                                  }
                    }
                else:
                    json_formated[json_title_key] = td_text.replace('Depuis', ' Depuis')

            except StopIteration:
                break

    return json_formated


# * ---------- Apply OCR on a scan ---------- *
# Get the scan as a pdf, then extract a JPG then apply OCR and return a string
def apply_ocr(pdf_path_file):
        path_img = f'../assets/img/TEMPS-IMG.jpg'
        path_dir_img = '../assets/img/'

        # Convert pdf to jpg
        with Img(filename=pdf_path_file, resolution=300) as img:
            img.compression_quality = 99
            img.save(filename=path_img)

        # Apply OCR on it
        text_from_pdf = ''
        for r, d, f in os.walk(path_dir_img):
            for img in f:
                if '.jpg' in img:
                    text_file = pytesseract.image_to_string(Image.open(path_dir_img + img))
                    text_from_pdf += text_file
                    os.remove(path_dir_img + img)

        return text_from_pdf


# * ---------- Language detection ---------- *
# Detect the language and return a string (formated like: "EN", "FR",...)
def detect_language(texte_string):
    # Load english in spacy
    nlp = spacy.load("en_core_web_sm")
    # Add the language detection
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
    # Apply NLP on the string
    string_with_nlp = nlp(texte_string)
    # Target the language NLP feature
    language_detected = string_with_nlp._.language
    return language_detected['language']


# * ---------- Get business number from company name ---------- *
# Scrap staatsbladmonitor.be to get name + business number + bank account from string input value.
# Return a Json with a name and a business number
def business_number_from_name(input_name_string):
    output_json = {}

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
        # Store data in a json format
        output_json[k] = {}
        output_json[k]['companyName'] = company_name
        output_json[k]['businessNumber'] = company_business_number

        # company_account_number = re.findall('BE[0-9]{4}\.[0-9]{3}\.[0-9]{3}', v.get_text())[0]
        # output_json[k]['account number'] = company_account_number

    return output_json

