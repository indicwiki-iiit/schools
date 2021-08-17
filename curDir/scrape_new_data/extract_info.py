# Scrapes data from urls of schools for available ids from schools.org.in
from bs4 import BeautifulSoup as bf
import requests
import pandas as pd
import time
import sys
import os
import pickle

# Global variables
start_index = 0
url_df = pd.DataFrame()
with open('schools_id_name_url_dataframe.pkl', 'rb') as f:
    url_df = pickle.load(f)
upper_limit = len(url_df["School Code"].tolist())
end_index = upper_limit

# Creating dataframe for given schools
def get_df(given_list):
    if len(given_list) < 1:
        return pd.DataFrame()
    df = given_list[0].T
    for i in range(1, len(given_list)):
        curr_id_df = given_list[i].T
        df = pd.concat([df, curr_id_df], axis=1)
    final_df = df.T
    final_df.drop(columns=["UDISE Code"], inplace=True)
    return final_df

# Saving dataframe for given schools data
def save_schools_data(initial_df1, schools_data):
    global start_index
    global end_index
    new_df = get_df(schools_data)
    new_initial_df1 = pd.concat([initial_df1, new_df], axis=0)
    new_initial_df1.to_excel(f'./schools_org_data_{start_index}-{end_index}.xlsx', index=False)
    return new_initial_df1

def main():
    global start_index
    global end_index
    global url_df
    if len(sys.argv) != 1 and len(sys.argv) != 3:
        print("Invalid arguments passed!")
        return
    if len(sys.argv) == 3:
        start_index = max(0, min(upper_limit, int(sys.argv[1])))
        end_index = max(0, min(upper_limit, int(sys.argv[2])))
        if start_index > end_index:
            print("Invalid arguments passed!")
            return
    url_df = url_df[start_index:end_index]
    # Obtain urls which have been obtained via web-crawling
    initial_df1 = pd.DataFrame()
    ids_to_be_processed = url_df["School Code"].tolist()
    if os.path.isfile(f'./schools_org_data_{start_index}-{end_index}.xlsx'):
        initial_df1 = pd.read_excel(f'./schools_org_data_{start_index}-{end_index}.xlsx')
        ids_to_be_processed = [_id for _id in url_df["School Code"].tolist() if not int(_id) in initial_df1["School Code"].tolist()]  
    schools_data = []
    school_done = 0
    ids_to_be_processed = list(set(ids_to_be_processed))
    consecutive_failures = 0
    for idx, row in url_df.iterrows():
        _id = row["School Code"]
        # print(_id)
        url = row["URL"]
        time.sleep(0.05)
        given_page = bf('<p></p>', "html.parser")
        try_count = 0
        while try_count < 5:
            try:
                given_url_output = requests.get(url, timeout = 120)
                given_page = bf(given_url_output.text, "html.parser")
                break
            except Exception as e:
                print(e)
                try_count += 1                
                time.sleep(5)
                pass
        if try_count == 5:
            consecutive_failures += 1
            if consecutive_failures >= 5:
                break
            else:
                continue
        consecutive_failures = 0
        new_attributes = ["School Code"]
        new_data = [[_id]]
        # Obtain attribute and corresponding value for all new data
        try:
            all_list_items = given_page.find_all('li', class_='list-group-item')
            for li in all_list_items:
                bold_text = ''
                try:
                    bold_text = li.find('b').text.strip()
                except:
                    pass
                normal_text = li.text.replace(':', '').strip()
                if bold_text == 'Meal':
                    bold_text = ' '.join(normal_text.split()[1:])
                    normal_text = 'Meal'
                else:
                    bold_text_tokens = 0
                    if len(bold_text) > 0:
                        bold_text_tokens = len(bold_text.split())
                    if bold_text_tokens > 0:
                        normal_text = ' '.join(normal_text.split()[:-bold_text_tokens])
                new_attributes.append(normal_text)
                new_data.append(bold_text)
        except:
            pass
        # Obtain title
        school_title = ""
        try:
           school_title = given_page.find('span', class_='shd').text.strip()
        except:
            pass
        new_attributes.append("School Title")
        new_data.append([school_title])
        # Obtain contact info
        try:
            contact_heading = given_page.find("h5")
            contact_headings = given_page.find_all("h5")
            for h in contact_headings:
                if "Contact" in h.text:
                    contact_heading = h
                    break
            contact_details = contact_heading.findNext('center')
            contact_tokens = contact_details.text.split(" ")
            for i in range(len(contact_tokens)):
                if i > len(contact_tokens) - 2 or i == 0:
                    continue
                if contact_tokens[i] == 'Code:' and contact_tokens[i-1].endswith("PIN"):
                    new_attributes.append("PIN Code")
                    new_data.append([contact_tokens[i+1] + ' ' + contact_tokens[i+2]])
                if contact_tokens[i].endswith('Mobile:') and not "XX" in contact_tokens[i+2]:
                    new_attributes.append("Mobile")
                    new_data.append([contact_tokens[i+1] + ' ' + contact_tokens[i+2]])
        except:
            pass
        # Obtain details of schools nearby
        try:
            nearby_schools = []
            nearby_school_anchor_tags = given_page.find_all('a', class_='p-1')
            for anchor_tag in nearby_school_anchor_tags:
                s_url = ""
                if anchor_tag.has_attr("href"):
                    s_url = "https://schools.org.in/" + anchor_tag["href"]
                s_name = anchor_tag.find('big').text.strip()
                nearby_schools.append(s_name + " #$# " + s_url)
            new_attributes.append("Nearby Schools")
            new_data.append([nearby_schools])
        except:
            pass      
        # Create df out of above data
        curr_row = dict(zip(new_attributes, new_data))
        curr_id_df = pd.DataFrame(curr_row, index=None)
        schools_data.append(curr_id_df)
        school_done += 1
        if school_done % 200 == 0:
            # Saving dataframe for every 200 schools
            print(f'{school_done} schools are done')
            initial_df1 = save_schools_data(initial_df1, schools_data)
            schools_data = []
            time.sleep(5)
    # Saving dataframe for schools processed after last save (to ensure data is not lost)
    initial_df1 = save_schools_data(initial_df1, schools_data)
    with open(f'./schools_org_data_{start_index}-{end_index}.pkl', 'wb') as f:
        pickle.dump(initial_df1, f)
        
if __name__ == '__main__':
	main()