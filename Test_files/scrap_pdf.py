# %% md
## Setup + Imports
# %%
import urllib, json
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
from tika import parser
import codecs
import re
import sys
# download pdf's urls
from datetime import datetime
import time
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
YEAR_LIST = [2014, 2015, 2016, 2017, 2018, 2019]

# get list of url from maxim's github
for YEAR in YEAR_LIST:
    print(f'* ____________________________ STARTING YEAR: {YEAR} ____________________________ *')
    url = f"https://raw.githubusercontent.com/GraphtyLove/KPMG-Challenge/master/assets/json/links_entreprises/links_entreprises_{YEAR}.json"
    response = urlopen(url)
    data = json.loads(response.read())
    data = list(set(data))

    ## Dowload PDF
    # %%
    for i, link in enumerate(data[:5]):
        try:
            time.sleep(0.1)
            reg_url = link
            req = Request(url=reg_url, headers=headers)
            html = urlopen(req).read()
            soup = BeautifulSoup(html, 'lxml')
            hrefs = soup.find_all('a', attrs={"target": "_blank"})
            pdf_url = hrefs[3].attrs['href']

            monitor_url = 'mopdf'
            if (monitor_url in pdf_url):
                print(f'ERROR, suspected monitor from url {i} {pdf_url}')
            else:
                myfile = requests.get(pdf_url)
                with open(f'../assets/pdf/{YEAR}/pdf-{i}.pdf', 'wb') as file:
                    file.write(myfile.content)

                print(f"PDF n°{i} OK from -> {link}")

        except:
            print(f'ERROR url: {i} {link}')
            print(sys.exc_info())

    ## Check all the PDF and sort a list of there names
    # %%

    file_number = []
    pdf_path = f'../assets/pdf/{YEAR}/'

    for r, d, f in os.walk(pdf_path):
        for file in f:
            if '.pdf' in file:
                file_number.append(re.findall('[0-9]+', file)[0])
    # Array of all PDF number as string
    file_number.sort(key=int)
    suspected_scans = []
    for number in file_number:
        file_path = pdf_path + 'pdf-' + number + '.pdf'
        try:
            raw = parser.from_file(file_path)
            text_len = len(raw['content'])
            if text_len < 1000:
                print(f'suspected scan: {number}')
                suspected_scans.append(number)
            else:
                with codecs.open(f'../assets/txt/{YEAR}/txt-{number}.txt', 'w', 'utf-8') as file:
                    file.write(raw['content'])
                print(f'file N° {number} -> len: {text_len}')
        except:
            print(f'ERROR with: {number}')
            print(sys.exc_info())
    with open(f'../assets/json/suspected_scans/suspected_scans_{YEAR}.json', 'w', encoding='utf-8') as file:
        json.dump(suspected_scans, file, ensure_ascii=False, indent=4)


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