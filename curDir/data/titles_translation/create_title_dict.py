# This script contains code for tokenizing english titles and storing their translations in a pickle file
import pickle
import pandas as pd

# Pre-processing for proper tokenization
def clean_string(given_string):
    new_string = given_string.replace("( ", "(").replace(" )", ")").replace(")", ") ").replace("(", " (")
    new_string = new_string.replace(' .', '.').replace('.', '. ').replace(' ,', ',').replace(',', ', ')
    to_replace = set([new_string[i-1] + new_string[i] for i in range(1, len(new_string))
                  if str(new_string[i]).isdigit() and not (str(new_string[i-1]).isdigit() or str(new_string[i-1]).isspace())])
    for s in to_replace:
        new_string = new_string.replace(s, s[0] + " " + s[1])
    new_string = new_string.replace('. )', '.)')
    new_string = new_string.replace(', )', ',)')
    all_tokens = [tok for tok in new_string.split() if len(tok) > 0 and tok != ' ']
    return str(' '.join(all_tokens)).strip(' \n\t\r')

# Handles special characters (especially in abbreviations) such as , and . such that one-one mapping is done as efficiently as possible
def handle_symbol_merging(current_list, symbol):
    new_list = []
    current_abbreviation = ""
    for token in current_list:
        if token.endswith(symbol):
            current_abbreviation += token
        else:
            if len(current_abbreviation) > 0:
                new_list.append(current_abbreviation)
            current_abbreviation = ""
            new_list.append(token)
    if(len(current_abbreviation)) > 0:
        new_list.append(current_abbreviation)
    return new_list

# Global variables with token mappings / edge cases
frequent_tokens = {}
edge_cases = {}
final_dict = {}

# Cleaning up keys of frequent tokens and storing so that they can be exploited when one-one mapping is not possible
freqTokens = pickle.load(open('../freqTokens.pkl', 'rb'))
for tok in freqTokens:
    frequent_tokens[clean_string(tok)] = freqTokens[tok]

# Obtaining the lists of english and telugu titles and codes
a = pd.read_excel('title0-21060.xlsx')
english_titles = a['పాఠశాల పేరు ఇంగ్లీష్ '].tolist()
telugu_titles = a['సవరించిన తెలుగు పేరు (ఇక్కడ అవసరం అయిన మార్పులు చేయగలరు)'].tolist()
codes = a['CODE '].tolist()

# Some edge cases which are being hardcoded
initial_abbreviations = {
    '(ZPHS)': '(ZPHS)', '(APMS)': '(APMS)', '(GPS)': ') last', '(MPPS)': '(MPPS)', '(MPUPS)': '(MPUPS)', 
    '(ZPPHS)': '(ZPPHS)', '(ZPOHS)': '(ZOPHS)', '(ZPOPS)': '(ZPOHS)'
}
final_dict['GPS'] = 'ప్రభుత్వ ప్రాథమిక పాఠశాల (గిరిజన సంక్షేమ) (GPS)'

perfect_one_to_one_mappings = 0
improper_mappings = 0

for i in range(len(english_titles)):
    # Tokenizing english and telugu titles
    english_title = clean_string(english_titles[i])
    telugu_title = clean_string(telugu_titles[i])
    current_code = codes[i]
    # print(f'{english_title} ==== {telugu_title}')
    english_tokens = [token for token in english_title.split() if len(token) > 0 and token != ' ']
    telugu_tokens = [token for token in telugu_title.split() if len(token) > 0 and token != ' ']
    
    # edge cases
    if english_title == "MPPS (GPS) SANKARAGUPTHAM":
        final_dict['(GPS)'] = 'ప్రభుత్వ ప్రాథమిక పాఠశాల (GPS)'
        final_dict['SANKARAGUPTHAM'] = 'శంకరగుప్తం'
        continue
    if len(english_tokens) == 0 or len(telugu_tokens) == 0:
        continue

    # Handling the case where first token of english title is an abbreviation and appears again in telugu title in brackets
    # (for proceeding to next tokens for one-one mapping)
    initial_abbreviation = '(' + english_tokens[0] + ')'
    if initial_abbreviation in initial_abbreviations.keys():
        if english_tokens[0] == 'GPS' or not initial_abbreviations[initial_abbreviation] in telugu_tokens:
            idx = 0
            for j in range(len(telugu_tokens)):
                if telugu_tokens[j].endswith(")"):
                    idx = j
            telugu_tokens = telugu_tokens[idx+1:]
            if english_tokens[0] != 'GPS':
                final_dict[english_tokens[0]] = ' '.join(telugu_tokens[:idx+1])
        else:
            end_of_abbreviation = telugu_tokens.index(initial_abbreviations[initial_abbreviation])
            final_dict[english_tokens[0]] = ' '.join(telugu_tokens[:end_of_abbreviation+1])
            telugu_tokens = telugu_tokens[end_of_abbreviation+1:]
        english_tokens = english_tokens[1:]
    
    # Handling . and , in both title tokens so that the mapping would be more consistent and accurate, and abbreviations info is not lost 
    # (undoing the split done while cleaning)
    english_tokens = handle_symbol_merging(english_tokens, '.')
    english_tokens = handle_symbol_merging(english_tokens, ',')
    telugu_tokens = handle_symbol_merging(telugu_tokens, '.')
    telugu_tokens = handle_symbol_merging(telugu_tokens, ',')
    
    # print(f'{english_tokens} ==== {telugu_tokens}')
    
    if len(english_tokens) == len(telugu_tokens):
        # Perfect one-one mapping is possible here
        for j in range(len(english_tokens)):
            final_dict[english_tokens[j]] = telugu_tokens[j]
        perfect_one_to_one_mappings += 1
    else:
        # One-one mapping is not possible here
        if len([tok for tok in english_tokens if not tok in frequent_tokens]) > 0:
            # Edge case where one-one mapping is not possible and freqTokens is not helpful for mapping
            edge_cases[english_title] = telugu_title + ' #$# code = ' + str(current_code)
            improper_mappings += 1
        else:
            # Frequent tokens can be used for getting translated output of english tokens, for all tokens in english title
            for token in english_tokens:
                final_dict[token] = frequent_tokens[token]

# Storing final token mappings and edge cases in pickle file (as dict) and csv file (as dataframe) 
token_mappings_df = {"English_title_token": [], "Telugu_title_token": []}
for k in final_dict:
    token_mappings_df["English_title_token"].append(k)
    token_mappings_df["Telugu_title_token"].append(final_dict[k])
edge_cases_df = {"Code": [], "English_titles": [], "Telugu_titles": []}
for k in edge_cases:
    edge_cases_df["English_titles"].append(k)
    edge_cases_df["Telugu_titles"].append(edge_cases[k].split(' #$# code = ')[0])
    edge_cases_df["Code"].append(edge_cases[k].split(' #$# code = ')[1])
pd.DataFrame.from_dict(token_mappings_df).to_csv("titleTokens.csv")
pd.DataFrame.from_dict(edge_cases_df).to_csv("edgeCases-titleTokens.csv")
with open('titleTokens.pkl', 'wb') as f:
    pickle.dump(final_dict, f)
with open('edgeCases-titleTokens.pkl', 'wb') as f:
    pickle.dump(edge_cases, f)

print(f'Total mappings done = {len(english_titles)}')
print(f'Perfect one to one mappings done = {perfect_one_to_one_mappings}')
print(f'Ignored improper mappings = {improper_mappings}')
print(f'Assisted mappings = {len(english_titles) - perfect_one_to_one_mappings - improper_mappings}')