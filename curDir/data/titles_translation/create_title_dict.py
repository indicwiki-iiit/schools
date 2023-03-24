# This script contains code for tokenizing english titles and storing their translations in a pickle file
import pickle
import pandas as pd

# telugu representation of english alphabets
telugu_letters = {
    "ఏ":'A', "ఎ":'A', "బి":'B', "బీ":'B', "సి":'C', "సీ":'C', "డి":'D', "డీ":'D', "ఇ":'E', 
    "ఈ":'E', "ఎఫ్":'F', "జి":'G', "జీ":'G', "హెచ్":'H', "ఐ":'I', "జె":'J', "జే":'J', 
    "కె":'K', "కే":'K', "ఎల్":'L', "ఎం":'M', "ఎమ్":"M", "యం":'M', "ఎన్":'N', "ఒ":'O', "ఓ":'O', "పి":'P', 
    "పీ":'P', "క్యు":'Q', "క్యూ":'Q', "అర్":'R', "ఆర్":'R', "ఎస్":'S', "టి":'T', "టీ":'T', 
    "యు":'U', "యూ":'U', "వి":'V', "వీ":'V', "డబ్ల్యూ":'W', "ఎక్స్":'X', "వై":'Y', "జెడ్":'Z'
}

# Global variables with token mappings / edge cases, frequent abbreviations and tokens
frequent_tokens = {}
frequent_telugu_abbreviations = {}

# Checks if given argument is indeed a valid string
def is_valid_string(attribute_value):
    if not isinstance(attribute_value, str) and not isinstance(attribute_value, float) and not isinstance(attribute_value, type(None)):
        return True
    return not (attribute_value == None or pd.isnull(attribute_value) or str(attribute_value) == "" or str(attribute_value) == "nan")

# Pre-processing for proper tokenization
def clean_string(given_string):
    new_string = given_string.replace("( ", "(").replace(" )", ")").replace(")", ") ").replace("(", " (")
    new_string = new_string.replace(' .', '.').replace('.', '. ').replace(' ,', ',').replace(',', ', ')
    to_replace = set([new_string[i-1] + new_string[i] for i in range(1, len(new_string))
                  if str(new_string[i]).isdigit() and not (str(new_string[i-1]).isdigit() or str(new_string[i-1]).isspace())])
    for s in to_replace:
        new_string = new_string.replace(s, s[0] + " " + s[1])
    new_string = new_string.replace('. )', '.)').replace(', )', ',)')
    # additional corner cases
    new_string = new_string.replace('ఉన్నత', ' ఉన్నత')
    new_string = new_string.replace('VIDYA NIKETHAN', 'VIDYANIKETHAN')
    all_tokens = [tok for tok in new_string.split() if len(tok) > 0 and tok != ' ']
    return str(' '.join(all_tokens)).strip(' \n\t\r')

# Handles special characters (especially in abbreviations) such as , and . such that one-one mapping is done as efficiently as possible
# (merging contiguous tokens ending with the same symbol: , or .)
def handle_symbol_merging(current_list, symbol):
    new_list = []
    current_abbreviation = ""
    for token in current_list:
        if token.endswith(symbol) or (len(token) >= 2 and token.endswith(symbol + ')')):
            current_abbreviation += token
        else:
            if len(current_abbreviation) > 0:
                new_list.append(current_abbreviation)
            current_abbreviation = ""
            new_list.append(token)
    if(len(current_abbreviation)) > 0:
        new_list.append(current_abbreviation)
    return new_list

# Cleaning up keys of frequent tokens and storing so that they can be exploited when one-one mapping is not possible
def obtain_frequent_tokens():
    global frequent_tokens
    freqTokens = pickle.load(open('../freqTokens.pkl', 'rb'))
    for tok in freqTokens:
        frequent_tokens[clean_string(tok)] = clean_string(freqTokens[tok])

# few acronymns (and their corresponding telugu tokens) which are used very frequently 
# (cases where a single english token is mapped to multiple telugu tokens - freqTokens are used only for very few recurring english tokens)
def obtain_frequent_telugu_abbreviations():
    global frequent_telugu_abbreviations
    global telugu_letters
    freqTokens_df = pd.read_csv('../freqTokens.csv')
    freqTokens_df = freqTokens_df.loc[freqTokens_df["Count"] >= 10]
    for i, row in freqTokens_df.iterrows():
        current_english_token = clean_string(freqTokens_df.at[i, "Eng Token"])
        if len(current_english_token) == 1 and current_english_token[0] >= 'A' and current_english_token[0] <= 'Z':
            current_english_token += '.'
        if not is_valid_string(freqTokens_df.at[i, "Telugu"]):
            continue
        current_telugu_translation = clean_string(freqTokens_df.at[i, "Telugu"])
        if current_telugu_translation in telugu_letters and not current_telugu_translation.endswith('.'):
            current_telugu_translation += '.'
        tokenized_telugu_string = handle_symbol_merging(current_telugu_translation.split(), '.')
        frequent_telugu_abbreviations[current_english_token] = len(tokenized_telugu_string)  
    # Rectifying some mistakes (via hardcoding directly in dict) in freqTokens
    frequent_telugu_abbreviations["EM"] = 2
    frequent_telugu_abbreviations["(EM)"] = 2

# Tries to rectify inconsistent mapping of english abbreviations to telugu 
# (handling cases like "AB CD" being mapped to "ఏ.బి.సి.డి.")
def improve_abbreviation_handling(english_tokens, telugu_tokens):
    global telugu_letters
    new_telugu_tokens = []
    english_tokens_pointer = 0
    for m in range(len(telugu_tokens)):
        # corner case
        if english_tokens_pointer >= len(english_tokens):
            new_telugu_tokens.append(telugu_tokens[m])
            continue
        # if current token is not a telugu abbreviation, ignore it
        if not '.' in telugu_tokens[m]:
            new_telugu_tokens.append(telugu_tokens[m])
            english_tokens_pointer += 1
            continue
        split_telugu_abbreviation = [t + '.' for t in telugu_tokens[m].split('.') if len(t) > 0 and t != ' ']
        # if current abbreviation is not telugu representation of english alphabet, ignore it
        if len([t for t in split_telugu_abbreviation if not t[:-1] in telugu_letters]) > 0:
            new_telugu_tokens.append(telugu_tokens[m])
            english_tokens_pointer += 1
            continue
        # Keep on splitting current telugu abbreviation until its in sync with corresponding english version 
        segments_to_split = []
        telugu_tok_count = len(split_telugu_abbreviation)
        while english_tokens_pointer < len(english_tokens) and telugu_tok_count > 0:
            current_english_tok = len([c for c in english_tokens[english_tokens_pointer] if c >= 'A' and c <= 'Z'])
            split_length = min(telugu_tok_count, current_english_tok)
            segments_to_split.append(split_length)
            telugu_tok_count -= split_length
            english_tokens_pointer += 1
        # corner case
        if telugu_tok_count != 0:
            new_telugu_tokens.append(telugu_tokens[m])
            continue
        # Actual split of telugu abbreviation and appending it to new telugu tokens
        current_pointer = 0
        for s in segments_to_split:
            new_telugu_tokens.append(''.join(split_telugu_abbreviation[current_pointer:current_pointer+s]))
            current_pointer += s
    return new_telugu_tokens

# Tries to rectify inconsistent mapping of english abbreviations to telugu 
# (handling cases like "PS" being mapped to "ప్రాథమిక పాఠశాల")
def improve_abbreviation_handling_2(english_tokens, telugu_tokens):
    global frequent_telugu_abbreviations
    new_telugu_tokens = []
    telugu_tokens_pointer = 0
    english_tokens_pointer = 0
    while telugu_tokens_pointer < len(telugu_tokens):
        # corner case
        if english_tokens_pointer >= len(english_tokens):
            new_telugu_tokens.append(telugu_tokens[telugu_tokens_pointer])
            telugu_tokens_pointer += 1
            continue
        # if current token is not a recurring english token, ignore it
        if not english_tokens[english_tokens_pointer] in frequent_telugu_abbreviations:
            new_telugu_tokens.append(telugu_tokens[telugu_tokens_pointer])
            english_tokens_pointer += 1
            telugu_tokens_pointer += 1
            continue
        # Keep on merging telugu tokens to be in sync with current english token 
        join_length = min(len(telugu_tokens) - telugu_tokens_pointer, frequent_telugu_abbreviations[english_tokens[english_tokens_pointer]])
        new_telugu_tokens.append(' '.join(telugu_tokens[telugu_tokens_pointer:telugu_tokens_pointer+join_length]))
        english_tokens_pointer += 1
        telugu_tokens_pointer += join_length
    return new_telugu_tokens

def create_tokenwise_mapping():
    global telugu_letters
    global frequent_tokens
    
    # Token mappings / edge cases
    edge_cases = {}
    final_dict = {}
    # Some edge cases which are being hardcoded via global variables
    initial_abbreviations = {
        '(ZPHS)': '(ZPHS)', '(APMS)': '(APMS)', '(GPS)': ')', '(MPPS)': '(MPPS)', '(MPUPS)': '(MPUPS)', 
        '(ZPPHS)': '(ZPPHS)', '(ZPOHS)': '(ZOPHS)', '(ZPOPS)': '(ZPOHS)'
    }
    final_dict['GPS'] = 'ప్రభుత్వ ప్రాథమిక పాఠశాల (గిరిజన సంక్షేమ) (GPS)' 
    # Keeps track of number of perfect and imperfect mappings
    perfect_one_to_one_mappings = 0
    improper_mappings = 0
    
    # Storing frequent tokens and abbreviations
    obtain_frequent_tokens()
    obtain_frequent_telugu_abbreviations()
    
    # Obtaining the lists of english and telugu titles and codes
    a = pd.read_excel('title0-21060.xlsx')
    english_titles = a['పాఠశాల పేరు ఇంగ్లీష్ '].tolist()
    telugu_titles = a['సవరించిన తెలుగు పేరు (ఇక్కడ అవసరం అయిన మార్పులు చేయగలరు)'].tolist()
    codes = a['CODE '].tolist()
    
    for i in range(len(english_titles[:])):
        # Tokenizing english and telugu titles
        english_title = clean_string(english_titles[i])
        telugu_title = clean_string(telugu_titles[i])
        current_code = codes[i]
        english_tokens = [token for token in english_title.split() if len(token) > 0 and token != ' ']
        telugu_tokens = [token for token in telugu_title.split() if len(token) > 0 and token != ' ']
        
        # Single lettered english alphabets are treated as abbreviations for efficient mapping
        for j in range(len(english_tokens)):
            if len(english_tokens[j]) == 1 and english_tokens[j][0] >= 'A' and english_tokens[j][0] <= 'Z' and english_tokens[j][0] != 'S':
                english_tokens[j] = english_tokens[j] + '.'
                
        # Single lettered representation of telugu alphabets are treated as abbreviations for efficient mapping
        for j in range(len(telugu_tokens)):
            if telugu_tokens[j] in telugu_letters and not telugu_tokens[j].endswith('.'):
                telugu_tokens[j] = telugu_tokens[j] + '.'
        
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
        
        # Handling . in both title tokens so that the mapping would be more consistent and accurate, and abbreviations info is not lost 
        # (undoing the split done while cleaning)
        english_tokens = handle_symbol_merging(english_tokens, '.')
        telugu_tokens = handle_symbol_merging(telugu_tokens, '.')
        telugu_tokens = improve_abbreviation_handling(english_tokens, telugu_tokens)
        telugu_tokens = improve_abbreviation_handling_2(english_tokens, telugu_tokens)    
        # print(english_tokens)
        # print(telugu_tokens)
        
        if len(english_tokens) == len(telugu_tokens):
            # Perfect one-one mapping is possible here
            for j in range(len(english_tokens)):
                final_dict[english_tokens[j]] = telugu_tokens[j]
            if len(english_tokens[j]) == 2 and english_tokens[j][0] >= 'A' and english_tokens[j][0] <= 'Z' and english_tokens[j][1] == '.':
                final_dict[english_tokens[j][0]] = telugu_tokens[j]
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
    pd.DataFrame.from_dict(token_mappings_df).to_excel("titleTokens.xlsx")
    pd.DataFrame.from_dict(edge_cases_df).to_csv("edgeCases-titleTokens.csv")
    pd.DataFrame.from_dict(edge_cases_df).to_excel("edgeCases-titleTokens.xlsx")
    with open('titleTokens.pkl', 'wb') as f:
        pickle.dump(final_dict, f)
    with open('edgeCases-titleTokens.pkl', 'wb') as f:
        pickle.dump(edge_cases, f)

    print(f'Total mappings done = {len(english_titles)}')
    print(f'Perfect one to one mappings done = {perfect_one_to_one_mappings}')
    print(f'Ignored improper mappings = {improper_mappings}')
    print(f'Assisted mappings = {len(english_titles) - perfect_one_to_one_mappings - improper_mappings}')

if __name__ == '__main__':
	create_tokenwise_mapping()