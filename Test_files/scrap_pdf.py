"""This script scrapes a website and saves pdfs of companies status, sorted by year, as well as corresponding metadata
path to pdfs: assets/pdf/
path to meta-data : assets/json/meta-data"""

import urllib, json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
import codecs
import re
import sys

from datetime import datetime
import time
import requests
import datetime
import numpy as np

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'
}
YEAR_LIST = [2017]

# get list of url from maxim's github
for YEAR in YEAR_LIST:
    print(f'°º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸ STARTING YEAR: {YEAR} °º¤ø,¸¸,ø¤º°`°º¤ø,¸,ø¤°º¤ø,¸¸,ø¤º°`°º¤ø,¸')
    url = f"https://raw.githubusercontent.com/" \
        f"GraphtyLove/KPMG-Challenge/master/assets/json/links_entreprises/links_entreprises_{YEAR}.json"
    response = urlopen(url)
    data = json.loads(response.read())
    data = list(set(data))
    data.sort()

    time_deltas = []
    saved_time = datetime.datetime.now()
    # Download PDF
    for i, link in enumerate(data):
        soup = None
        try:
            # calculte ETA
            time_deltas.insert(0, datetime.datetime.now() - saved_time)
            time_deltas = time_deltas[:1000]
            time_delta = np.mean(time_deltas)
            saved_time = datetime.datetime.now()

            print(f'________________ file {i} / {len(data)} ________________ ETA: '
                  f'{time_delta * (len(data) - i)} ________________')
            print(f'link: {link}')

            time.sleep(0.1)
            reg_url = link
            req = Request(url=reg_url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')

            pdf_url = soup.find('td', text="Oprichtingsakte").findNext('td').findNext('td').findChildren('a')[0].attrs[
                'href']
            print('                     pdf_url: ', pdf_url)

            monitor_url = 'mopdf'
            if monitor_url in pdf_url:
                print(f'               (¬_¬) suspected monitor pdf')
            else:
                my_file = requests.get(pdf_url)
                with open(f'../assets/pdf/{YEAR}/pdf-{i}.pdf', 'wb') as file:
                    file.write(my_file.content)

                print("               (⚗_⚗) pdf successfully scraped")
        except:
            print("          (ಠ۾ಠ) Error on scraping the pdf")
            print('                   ', sys.exc_info())

        # Scrape metadata and save it to json

        try:
            meta_data = {}
            title = soup.find_all('td', attrs={"class": "title"}, text=True)
            m_data = soup.find_all('td', attrs={"colspan": "2"}, text=True)

            smaller_len = min(len(m_data), len(title))
            for k in range(smaller_len):
                value = m_data[k].getText()
                value_as_string = str(value)
                if "Laatste" not in value_as_string:
                    meta_data[title[k].getText()] = value_as_string

            # add the url to the metadata
            meta_data['url'] = link

            with open(f'../assets/json/meta-data/{YEAR}/{i}.meta.json', 'w', encoding='utf-8') as file:
                json.dump(meta_data, file, ensure_ascii=False, indent=4)

            print("               (⚗_⚗) meta-data successfully scraped")
        except:
            print("                (╯︵╰,) Error on scraping the metadata")
            print('                   ', sys.exc_info())

    # %%
# ! -------------------- DEBUG -------------------- !


# * ---------- Find the key of a value ---------- *
# for k,v in enumerate(file_number):
#    if v == '2000':
#        print(f'key: {k} value: {v}')

# %% md
## Re-process PDF -> TXT for ERRORS

# %%
# ####REWRITE THIS
# for number in error_files:
#     file_path = f'pdf/{number}.pdf'
#     while(True):
#         try:
#             raw = parser.from_file(file_path)
#             len_raw = len(raw['content'])

#             with codecs.open(f'txt/txt-{number}.txt', 'w', 'utf-8') as file:
#                     file.write(raw['content'])
#                     text_len = len(raw['content'])

#             #with codecs.open(f'txt/txt-{number}.txt', 'r','utf-8') as file:
#                 #text_len = len(file.read())
#             print(f'file N° {number} -> len: {text_len}')
#             if text_len > 1000:
#                 break
#             else:
#                 error_files.append(number)
#                 break
#         except:
#             print(f'ERROR with: {number}')
#             print(sys.exc_info())
# print(error_files)

# %% md
# ---------- DEBUG ----------

# %% md
## PDF -> TXT on a specifique file

# %%
# file_to_convert = 23932

# raw = parser.from_file(f'pdf/{file_to_convert}.pdf')
# raw_len = len(raw['content'])
# print(raw_len)

# with open(f'{file_to_convert}.txt', 'w') as file:
#     file.write(raw['content'])

# with open(f'{file_to_convert}.txt', 'r') as file:
#     txt_len = len(file.read())
#     print(txt_len)


# %% md
## Print the len of a file

# %%
# with open('txt/47.txt', 'r') as file:
#      print(len(file.read()))
