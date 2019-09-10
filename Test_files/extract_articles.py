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

class_1_files = []
for file_number in files_numbers[:1000]:
    with open(f'../assets/txt/{YEAR}/fr/txt-{file_number}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        # remove vertical text
        text = re.sub('[\n\r].{1,3}(?=[\n\r])', '', text)
        # limit newlines
        #text = re.sub('[\n\r]+', '\n', text)
        #match ARTICLE X followed by subject
        pattern = re.compile("(ARTICLE\s[0-9]+ .* \.?)")
        regex_matches = re.findall(pattern, text)
        n_regex_matches = len(regex_matches)
        if (n_regex_matches > 2):
            print('¸.•* ¸.•* ¸.•* file {} has : {} matches *•.¸ *•.¸ *•.¸'
                  .format(file_number, n_regex_matches))
            for match in regex_matches:
                print(match)
            class_1_files.append(file_number)

print(f'class_1_files : {class_1_files}')

