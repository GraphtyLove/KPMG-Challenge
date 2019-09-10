import shutil
import os
import spacy
from spacy_langdetect import LanguageDetector
import re
import datetime
import numpy as np

# %%

for YEAR in range(2014, 2020):
    txt_path = f'../assets/txt/{YEAR}/'

    files = []

    for r, d, f in os.walk(txt_path):
        files.extend(f)
        break
    print(f'number of files in {txt_path} : ', len(files))
    print(files)
    # %%

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)

    saved_time = datetime.datetime.now()
    time_deltas = []
    for i, filename in enumerate(files):
        time_deltas.append(datetime.datetime.now() - saved_time)
        time_delta = np.mean(time_deltas)
        saved_time = datetime.datetime.now()
        print(f"¸.•* ¸.•* ¸.•* progress : {i}/{len(files)} ETA: {time_delta * (len(files) - i)} *•.¸ *•.¸ *•.¸")
        text = ''
        with open(txt_path + filename, 'r', encoding='utf-8') as file:
            text = file.read()
        doc = nlp(text)
        lg = doc._.language
        language = lg['language']
        try:
            shutil.move(txt_path + filename, txt_path + f'/{language}/' + filename)
        except FileNotFoundError:
            os.mkdir(txt_path + f'/{language}/')
            shutil.move(txt_path + filename, txt_path + f'/{language}/' + filename)
