import os
import re
import pandas as pd

# %%
YEAR = 2016
txt_path = f'../assets/txt/{YEAR}/fr/'

files_numbers = []

for r, d, f in os.walk(txt_path):
    for file in f:
        if '.txt' in file:
            files_numbers.append(re.findall('[0-9]+', file)[0])

# %%

gibberish_list = ["- suiteVolet B",
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

class_1_files = []
for file_number in files_numbers[:1000]:
    with open(f'../assets/txt/{YEAR}/fr/txt-{file_number}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        # remove vertical text
        text = re.sub('[\n\r].{1,3}(?=[\n\r])', '', text)
        # limit newlines
        # text = re.sub('[\n\r]+', '\n', text)

        for pattern in gibberish_list:
            text = re.sub(pattern, '', text)

        # match ARTICLE X followed by subject
        pattern = re.compile(r"(ARTICLE\s[0-9]+.*)")
        regex_matches = re.findall(pattern, text)
        n_regex_matches = len(regex_matches)
        if n_regex_matches > 2:
            print('¸.•* ¸.•* ¸.•* file {} has : {} matches *•.¸ *•.¸ *•.¸'
                  .format(file_number, n_regex_matches))
            for match in regex_matches:
                print(match)
            class_1_files.append(file_number)

print(f'class_1_files : {class_1_files}')
