import os
import re
import pandas as pd

# %%
YEAR = 2016
txt_path = f'../assets/txt/{YEAR}/fr/'

files_numbers = []
n_valid_files = 0
n_invalid_files = 0
df = pd.DataFrame(columns=['Doc_id', 'Title', 'Body'])

for r, d, f in os.walk(txt_path):
    for file in f:
        if '.txt' in file:
            files_numbers.append(re.findall('[0-9]+', file)[0])

files_numbers.sort(key=int)

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

for i, file_number in enumerate(files_numbers):
    print(f'### Progress: {i}/{len(files_numbers)}')
    with open(f'../assets/txt/{YEAR}/fr/txt-{file_number}.txt', 'r', encoding='utf-8') as file:
        text = file.read()
        # remove vertical text
        text = re.sub('[\n\r].{0,3}(?=[\n\r])', '', text)

        for pattern in gibberish_list:
            text = re.sub(pattern, '', text)

        # match ARTICLE X followed by subject
        pattern_title = re.compile(r"(?:ARTICLE|Article) .*")
        regex_matches_titles = re.findall(pattern_title, text)
        n_regex_matches_titles = len(regex_matches_titles)
        if n_regex_matches_titles > 2:
            n_valid_files += 1
            print('( ͡° ͜ʖ ͡°) file {} '
                  'has : {} matches'
                  .format(file_number, n_regex_matches_titles))

            # find the article body
            # It's easy to find the body, just take whats between two article titles, but that doesn't capture the
            # last article, so the last article, it captures the text to the end
            # TODO: make a model that truncates the last article match
            pattern_body = re.compile(r"(?:ARTICLE|Article) .*((?:\n.*)*?\n?\s*(?=ARTICLE|Article|^[A-Z][A-Z\.\s\-]{3,}$|\Z))")
            regex_matches_bodies = re.findall(pattern_body, text)
            for match_body, match_title in zip(regex_matches_bodies, regex_matches_titles):
                # print('          -`ღ´- <article match title: ' + match_title + '> -`ღ´-')
                # print('          -`ღ´- <article match body: ' + match_body + '>')
                df = df.append({'Title': match_title,
                                'Body': match_body,
                                'Doc_id': file_number}, ignore_index=True)
        else:
            n_invalid_files += 1
            print(f'(ノಠ益ಠ)ノ彡 file {file_number} has no matches (ノಠ益ಠ)ノ彡')

print(f'{n_valid_files} out of {len(files_numbers)}, {n_valid_files / len(files_numbers)}')
df.to_csv(f'../assets/csv/{YEAR}/fr/articles.csv')
