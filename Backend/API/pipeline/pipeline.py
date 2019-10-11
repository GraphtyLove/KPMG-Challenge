"""
* ========== PIPELINE ========== *

 | DL pdf | ===>
 | IF JPG -> apply OCR - ELSE extract TXT | ===>
 | Classify with lang | ===>
 | Extract article | ===>
 | Clean article |

"""

# * ========== IMPORT ========== *
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import sys
import requests
import os
from uuid import uuid1
from wand.image import Image as Img
import pytesseract
from PIL import Image
import codecs
from tika import parser
import spacy
from spacy_langdetect import LanguageDetector
import pandas as pd
import re
import unidecode
from numeral import roman2int
from text_to_num import alpha2digit
import numpy as np
from IPython.display import display
import shutil


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
                                json_formated[json_title_key][json_key] = td_text.replace('Dénomination',
                                                                                          ' Dénomination')

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

    json_formated["status"] = scrap_the_pdf(entreprise_number)

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

# * ========== DL PDF ========== *
# DL the PDF depending on the Business number.
def dl_pdf(business_number, uuid):
    print(f"Start Downloading PDF for company: {business_number}")

    all_goes_well = False

    # Link where we download PDF
    url = f'https://www.staatsbladmonitor.be/bedrijfsfiche.html?ondernemingsnummer={business_number}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
    }
    # Get the download link of the PDF
    try:
        req = Request(url=url, headers=headers)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'lxml')

        # Link of the PDF itself
        path_pdf = soup.find('td', text="Oprichtingsakte").findNext('td').findNext('td').findChildren('a')[0].attrs[
            'href']
        print(f'PDF url: {path_pdf}')

    except:
        print(f'!!! ERROR while DL PDF of company: {business_number}')
        print('CODE ERROR: ', sys.exc_info())

    # Check if PDF is usable and save the PDF in a temp folder
    try:
        # PDF that are formated as monitor (more then 200pages + too heavy)
        monitor_url = 'mopdf'

        if monitor_url in path_pdf:
            print('Unusable PDF (monitor formated)')
        else:
            # Get the file
            pdf_file = requests.get(path_pdf)

            # Create the folder in path
            try:
                path = f"{os.path.dirname(os.path.realpath(__file__))}/{uuid}"
                os.mkdir(path)
                path = f'{path}/pdf'
                os.mkdir(path)
            except:
                print(f'ERROR creating uuid folder')
                print('CODE ERROR: ', sys.exc_info())

            # Save PDF
            with open(f'{path}/pdf-{business_number}.pdf', 'wb') as file:
                file.write(pdf_file.content)
            all_goes_well = True
    except:
        print(f'ERROR saving PDF of company: {business_number} in path: ./temp/{uuid}/pdf-{business_number}.pdf')
        print('CODE ERROR: ', sys.exc_info())

    return all_goes_well


def check_for_ocr(business_number, uuid):
    # * ---------- PATH --------- *
    # Path of the this file
    path_file = os.path.dirname(os.path.realpath(__file__))
    # PDF url
    path_pdf = f"{path_file}/{uuid}/pdf/pdf-{business_number}.pdf"
    # Path to CREATE img
    path_img_dir = f'{path_file}/{uuid}/img'
    # Path to SAVE img
    path_img = f"{path_img_dir}/{business_number}.jpg"
    # Path to WALK img
    path_img_dir_walk = path_img_dir + '/'
    # Path to CREATE txt
    path_txt_dir = f'{path_file}/{uuid}/txt'
    # Path to SAVE txt
    path_txt_file = f'{path_txt_dir}/{business_number}-OCR.txt'
    # Path to READ txt from PDF file
    path_txt_file_from_pdf = f'{path_txt_dir}/{business_number}-FROM-PDF.txt'

    is_ocr_done = False

    # * ------------------- CHECK IF THIS IS A SCAN ------------------ *
    with open(path_txt_file_from_pdf, 'r', encoding='utf-8') as file:
        text = file.read()
    if len(text) < 1000:
        print("Processing OCR...")
        # * ---------- CREATE FOLDERS ---------- *
        # Create a img folder to store images
        os.mkdir(path_img_dir)

        # Convert pdf to jpg
        with Img(filename=path_pdf, resolution=300) as img:
            img.compression_quality = 99
            img.save(filename=path_img)

        # Apply OCR on it
        total_text = ''
        try:
            for r, d, f in os.walk(path_img_dir_walk):
                for img in f:
                    if '.jpg' in img:
                        print(f'{img} Converting...')
                        text_file = pytesseract.image_to_string(Image.open(path_img_dir_walk + img))
                        total_text += text_file
        except:
            print(f'!!! ERROR while OCR to PDF of company: {business_number} !!!')
            print('CODE ERROR: ', sys.exc_info())

        try:
            # Save text in a TXT directory
            with codecs.open(path_txt_file, 'w', 'utf-8') as file:
                file.write(total_text)
            print(f'PDF {business_number} well extracted.')
            is_ocr_done = True

        except:
            print(f'!!! ERROR while SAVING TXT of company: {business_number} !!!')
            print('CODE ERROR: ', sys.exc_info())
    return is_ocr_done


def extract_text_from_pdf(business_number, uuid):
    # * ---------- PATH --------- *
    # Path of the this file
    path_file = os.path.dirname(os.path.realpath(__file__))
    # PDF url
    path_pdf = f"{path_file}/{uuid}/pdf/pdf-{business_number}.pdf"
    # Path to SAVE txt
    path_txt_file = f'{path_file}/{uuid}/txt/{business_number}-FROM-PDF.txt'
    # Path to CREATE txt
    path_txt_dir = f'{path_file}/{uuid}/txt'


    # * ---------- CREATE FOLDERS ---------- *
    # Create a txt folder to store text
    os.mkdir(path_txt_dir)

    try:
        text_extracted = parser.from_file(path_pdf)
        with codecs.open(path_txt_file, 'w', 'utf-8') as file:
            file.write(text_extracted['content'])
        print(f'file N° {business_number} well extracted')
    except:
        print(f'ERROR with: {business_number} while text extraction from PDF')
        print('CODE ERROR: ', sys.exc_info())


def detect_language(uuid):
    languages_detected = []
    # * ---------- PATH --------- *
    # Path of the this file
    path_file = os.path.dirname(os.path.realpath(__file__))
    # Path to WALK txt
    path_txt_dir_walk = f'{path_file}/{uuid}/txt/'

    # Detect language of all the txt files and put them in languages_detected array
    for r, d, f in os.walk(path_txt_dir_walk):
        for txt in f:
            if '.txt' in txt:
                # Read the txt file to get the text
                with codecs.open(path_txt_dir_walk + txt, 'r', 'utf-8') as file:
                    txt_content = file.read()
                # Load Spacy
                nlp = spacy.load("en_core_web_sm")
                # Add language detection to it
                nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
                # Apply NLP on text
                txt_nlp = nlp(txt_content)
                # Target the language part of the nlp done
                txt_lang = txt_nlp._.language
                # Add the language detected to to languages_detected array
                languages_detected.append(txt_lang['language'])
    if 'fr' in languages_detected:
        is_languague_is_french = True
    else:
        is_languague_is_french = False

    return is_languague_is_french


def extract_articles(uuid):
    file_txt_name_list = []
    n_valid_files = 0
    n_invalid_files = 0

    # * ---------- PATH --------- *
    # Path of the this file
    path_file = os.path.dirname(os.path.realpath(__file__))
    # Path to WALK txt
    path_txt_dir_walk = f'{path_file}/{uuid}/txt/'


    df = pd.DataFrame(columns=['Doc_id', 'Title', 'Body'])

    # Get a list of the name of all the txt file
    for r, d, f in os.walk(path_txt_dir_walk):
        for file in f:
            if '.txt' in file:
                file_txt_name_list.append(file)

    useless_stuff_list = ["- suiteVolet B",
                            "Au verso : Nom et signature.",
                            "ayant pouvoir de représenter l'association ou la fondation à l'égard des tiers",
                            "Mentionner sur la dernière page du Volet B : Au recto : Nom et qualité du notaire instrumentant ou de la personne ou des personnes",
                            "Moniteur",
                            "belge",
                            "Réservé",
                            "au",
                            "Au verso : Nom et signature",
                            "Volet B - suite",
                            "Mod PDF 11.1",
                            " Volet B",
                            r"\*[0-9]+\*",
                            r"MOD [0-9]\.[0-9]",
                            "Copie à publier x annexes du",
                            "après dépôt de l'acte  greffe",
                            "Greffe"]
    # Process all the txt files
    for file_name in file_txt_name_list:
        with open(path_txt_dir_walk + file_name, 'r', encoding='utf-8') as file:
            text = file.read()

        # Remove vertical text
        text = re.sub('[\n\r].{0,3}(?=[\n\r])', '', text)

        # Remove useless stuff from the text
        for pattern in useless_stuff_list:
            text = re.sub(pattern, '', text)

        # * ---------- Get articles TITLE ---------- *
        # (match ARTICLE X followed by subject)
        pattern_title = re.compile(r"(?:ARTICLE|Article) .*")
        titles_matched = re.findall(pattern_title, text)
        titles_matched_len = len(titles_matched)
        if titles_matched_len > 2:
            n_valid_files += 1
            print(f'(File N° {file_name} has: {titles_matched_len} matches')

        # * ---------- Get articles BODY ---------- *
        # Get the text between two titles
        pattern_body = re.compile(
            r"(?:ARTICLE|Article) .*((?:\n.*)*?\n?\s*(?=ARTICLE|Article|^[A-Z][A-Z\.\s\-]{3,}$|\Z))")
        regex_matches_bodies = re.findall(pattern_body, text)

        # Match article's TITLE with BODY
        for match_body, match_title in zip(regex_matches_bodies, titles_matched):
            df = df.append({'Title': str(match_title),
                            'Body': match_body,
                            'Doc_id': file_name}, ignore_index=True)
        else:
            n_invalid_files += 1
    return df

def clean_articles(articles_dataframe):
    articles_dataframe['Title_len'] = articles_dataframe.Title.str.len()

    articles_dataframe['Extracted_Number'] = articles_dataframe.Title.str.extract(
        '(?:Article|ARTICLE)\s-?[:\s\.–]?\s?((?:[0-9]+|(?:'
        '(?:DIX|VINGT|TRENTE|QUARANTE|CINQUANTE|SOIXANTE|SEPTANTE|QUATRE-VINGT|NONANTE|TRENET|'
        '[Dd]ix|vingt|trente|quarante|cinquante|soixante|septante|quatre-vingt|nonante|viNGT|vINGT|'
        'ONZE|DOUZE|TREIZE|QUATORZE|QUINZE|SEIZE'
        '|[Oo]nze|[Dd]ouze|[Tt]reize|[Qq]uatorze|[Qq]uinze|[Ss]eize'
        '|PREMIER|DEUXI(?:È|E)ME|TROISI(?:È|E)ME|QUATRI(?:È|E)ME|CINQUI(?:È|E)ME|SIXI(?:È|E)ME'
        '|SEPTI(?:È|E)ME|HUITI(?:È|E)ME|NEUVI(?:È|E)ME|'
        'DIXI(?:È|E)ME|ONZI(?:È|E)ME|DOUZI(?:È|E)ME|TREIZI(?:È|E)ME|QUATORZI(?:È|E)ME|'
        'QUINZI(?:È|E)ME|SEIZI(?:È|E)ME|TRENTI(?:È|E)ME|QUARANTI(?:È|E)ME|CINQUANTI(?:È|E)ME'
        '|[XVIl]+|OUATRE|[Pp]remier|quatri(?:è|e)me'
        ')?[\s-]?\s?(?:ET|et)?[\s-]?(?:UN|DEUX|TROIS|QUATRE|CINQ|SIX|[Ss]EPT|HUIT|NEUF|'
        '[Uu]n|[Dd]eux|[Tt]rois|[Qq]uatre|[Cc]inq|[Ss]ix|[Ss]ept|[Hh]uit|[Nn]euf)?)))')

    replace_dic = {
        'vingt': 'vingt ',
        'trente': 'trente ',
        '-': ' ',
        'premier': '1',
        'dix': 'dix ',
        'VINGT': 'VINGT ',
        'PREMIER': '1',
        'TROISIEME': '3',
        'TRENTIEME ET UN': '31',
        'TRENTIEME': '30',
        'TRENTE': 'TRENTE ',
        'TRENET': 'TRENTE',
        'TREIZIEME': '13',
        'SIXIEME': '6',
        'SEPTIEME': '7',
        'SEIZIEME': '16',
        'QUINZIEME': '15',
        'QUATRIEME': '4',
        'QUATORZIEME': '14',
        'Premier': '1',
        'QUARANTIEME': '40',
        'OUATRE': '4',
        'ONZIEME': '11',
        'NEUVIEME': '9',
        'HUITIEME': '8',
        'DOUZIEME': '12',
        'DIX': 'DIX ',
        'DEUXIEME': '2',
        'CINQUIEME': '5'
    }

    def fix_spaces(s):
        for k in replace_dic.keys():
            s = s.replace(k, replace_dic[k])
        return s

    def sorter(s):
        if re.search('([0-9]+)', s):
            return re.search('([0-9]+)', s).group(0)
        else:
            return alpha2digit(s, relaxed=True)

    articles_dataframe['Extracted_Number_final'] = articles_dataframe.Extracted_Number.apply(fix_spaces).apply(
        sorter).apply(sorter)

    def parse_roman_num(s):
        s = str(s)
        if s == 'l':
            s = 'I'
        if re.search('(^[XIV]+$)', s):
            return str(roman2int(s))
        else:
            return s

    articles_dataframe['Extracted_Number_final'] = articles_dataframe['Extracted_Number_final'].apply(parse_roman_num)

    def remove_non_informative_part(title, number):
        return title[8 + len(number):]

    articles_dataframe['Extracted_Title'] = [remove_non_informative_part(x, y) for x, y in
                                           zip(articles_dataframe.Title, articles_dataframe.Extracted_Number)]

    # ieme does work
    rep_list = ['<<', '.', ':', '-', '–', ' ', '—', '•', '/', ',', '0', '$',
                '"', '§', '°', '~', '+', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', '0', '*']
    rep_list2 = ['𝑒', '𝑠', '.', ':', '_', '*', ';', '(...)', '•']
    rep_list3 = ['ème', 'er', 'bis', 'ieme', 'ième', 'ter', 'deg']

    def clean_title(s):
        if (s):
            for x in rep_list3:
                if s.startswith(x):
                    s = s[len(x):]
            for x in rep_list2:
                s = s.replace(x, '')
            s = unidecode.unidecode(s)
            while True:
                if (len(s) > 0) and s[0] in rep_list:
                    s = s[1:]
                else:
                    break
            return s.lower()
        else:
            return ''

    def deal_with_combinations(s):
        s = s.replace(' - ', ' + ').replace(' et ', ' + ').replace(' -- ', ' + ')
        return s

    articles_dataframe['Extracted_Title'] = articles_dataframe.Extracted_Title.apply(clean_title).apply(
        clean_title).apply(deal_with_combinations)

    articles_dataframe['Title_len'] = articles_dataframe.Extracted_Title.str.len()

    det_list = ["l'", 'le ', 'un ', 'les ', 'la ', 'tout ', 'en ', 'chaque ', 'tous ', 'pour ', 'aucun ', 'il ',
                'au ', 'dans ', 'si ']

    series_mask = [articles_dataframe.Extracted_Title.str.startswith(x) for x in det_list]
    mask_sum = np.zeros(series_mask[0].shape)
    for x in series_mask:
        mask_sum = np.logical_or(mask_sum, x)

    # Split the dataset
    articles_dataframe['Title_len'] = articles_dataframe.Extracted_Title.str.len()

    # put the title back to the body when necessary
    series_mask = [articles_dataframe.Extracted_Title.str.startswith(x) for x in det_list]
    mask_sum = np.zeros(series_mask[0].shape)
    for x in series_mask:
        mask_sum = np.logical_or(mask_sum, x)

    def add_title_to_body(title, body):
        return title + body

    articles_dataframe.loc[mask_sum, 'Body'] = [add_title_to_body(x, y) for x, y in
                                              zip(articles_dataframe[mask_sum].Extracted_Title,
                                                  articles_dataframe[mask_sum].Body)]

    articles_dataframe.loc[mask_sum, 'Extracted_Title'] = ''

    # articles_dataframe['Extracted_Number_final'] = articles_dataframe['Extracted_Number_final'].astype(str, errors='ignore')
    # print( articles_dataframe['Extracted_Number_final'].dtypes)
    articles_dataFrame_clean = articles_dataframe[['Extracted_Number_final', 'Extracted_Title','Body']]
    return articles_dataFrame_clean


# * ---------- Function that centralise all the others --------- *
def scrap_the_pdf(business_number):
    uui = uuid1()
    is_pdf_scraped = dl_pdf(business_number, uui)

    if is_pdf_scraped:
        extract_text_from_pdf(business_number, uui)
        is_ocr_done = check_for_ocr(business_number, uui)
        if is_ocr_done:
            path_pdf_file = f"{os.path.dirname(os.path.realpath(__file__))}/{uui}/pdf"
            shutil.rmtree(path_pdf_file, ignore_errors=True)
        is_french = detect_language(uui)
        if is_french:
            articles_dataFrame = extract_articles(uui)
            articles_dataFrame_clean = clean_articles(articles_dataFrame)
            print(articles_dataFrame.info())
            def rep(s):
                return s.replace('\n', ' ')
            articles_dataFrame_clean['Body'] = articles_dataFrame_clean['Body'].apply(rep)
            pdf_info_as_json = articles_dataFrame_clean.to_json(orient='records')



        else:
            print('File is not in french...')
            pdf_info_as_json = 'File is not in french...'

    else:
        print("no PDF to scrap")
        pdf_info_as_json = 'no PDF to scrap'
    # Delete the temp file that contain all the files we saved
    shutil.rmtree(f"{os.path.dirname(os.path.realpath(__file__))}/{uui}", ignore_errors=True)

    return pdf_info_as_json


# ! ========================= TEST ZONE ========================= !
# * --- OCR en FR --- *
# scrap_the_pdf('0475992757')
