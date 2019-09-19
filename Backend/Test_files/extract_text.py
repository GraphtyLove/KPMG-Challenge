import os
from tika import parser
import codecs
import re
import sys
# download pdf's urls
from datetime import datetime
import time
import requests
import json

YEAR_LIST = [2014, 2015, 2016, 2017, 2018, 2019]

for YEAR in YEAR_LIST:
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
