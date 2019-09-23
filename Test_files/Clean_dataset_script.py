def process_df(input_csv, output_csv):
    import pandas as pd

    df = pd.read_csv(input_csv)

    df['Title_len'] = df.Title.str.len()

    plain_text_number_pattern = ''
    df['Extracted_Number'] = df.Title.str.extract('(?:Article|ARTICLE)\s-?[:\s\.–]?\s?((?:[0-9]+|(?:'
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

    import re
    from text_to_num import alpha2digit

    def sorter(s):
        if re.search('([0-9]+)', s):
            return re.search('([0-9]+)', s).group(0)
        else:
            return alpha2digit(s, relaxed=True)

    df['Extracted_Number_final'] = df.Extracted_Number.apply(fix_spaces).apply(sorter).apply(sorter)

    from numeral import roman2int

    def parse_roman_num(s):
        s = str(s)
        if s == 'l':
            s = 'I'
        if re.search('(^[XIV]+$)', s):
            return str(roman2int(s))
        else:
            return s

    df['Extracted_Number_final'] = df['Extracted_Number_final'].apply(parse_roman_num)

    def remove_non_informative_part(title, number):
        return title[8 + len(number):]

    df['Extracted_Title'] = [remove_non_informative_part(x, y) for x, y in zip(df.Title, df.Extracted_Number)]

    import unidecode

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

    df['Extracted_Title'] = df.Extracted_Title.apply(clean_title).apply(clean_title).apply(deal_with_combinations)

    df['Title_len'] = df.Extracted_Title.str.len()

    det_list = ["l'", 'le ', 'un ', 'les ', 'la ', 'tout ', 'en ', 'chaque ', 'tous ', 'pour ', 'aucun ', 'il ',
                'au ', 'dans ', 'si ']
    import numpy

    series_mask = [df.Extracted_Title.str.startswith(x) for x in det_list]
    mask_sum = numpy.zeros(series_mask[0].shape)
    for x in series_mask:
        mask_sum = numpy.logical_or(mask_sum, x)

    # Split the dataset
    df['Title_len'] = df.Extracted_Title.str.len()
    df_predict = df[df.Title_len == 0]
    df_train = df[df.Title_len > 0]

    # put the title back to the body when necessary
    series_mask = [df.Extracted_Title.str.startswith(x) for x in det_list]
    mask_sum = numpy.zeros(series_mask[0].shape)
    for x in series_mask:
        mask_sum = numpy.logical_or(mask_sum, x)

    def add_title_to_body(title, body):
        return title + body

    df.loc[mask_sum, 'Body'] = [add_title_to_body(x, y) for x, y in
                                zip(df[mask_sum].Extracted_Title, df[mask_sum].Body)]

    df.loc[mask_sum, 'Extracted_Title'] = ''

    df['Extracted_Number_final'] = df['Extracted_Number_final'].astype(int, errors='ignore')

    saved_csv = df[['Doc_id', 'Extracted_Number_final', 'Extracted_Title', 'Body']].sort_values(
        by=['Doc_id', 'Extracted_Number_final'])
    saved_csv.to_csv(output_csv)
