# Scrapes url of schools for available ids from schools.org.in
from bs4 import BeautifulSoup as bf
import requests
import pandas as pd
import time
import pickle
import sys

base_url = "https://schools.org.in/"

# Given a url, get the source of that page and extract all links in the striped-table of that page
def get_table_urls(url):
    global base_url
    url_list = []
    time.sleep(2)
    given_url_output = requests.get(url)
    given_page = bf(given_url_output.text, "html.parser")
    anchor_tags_list = given_page.find('table', class_='table table-striped').find_all('a')
    for anchor_tag in anchor_tags_list:
        if not anchor_tag.has_attr("href"):
            continue
        url_list.append(base_url + anchor_tag["href"])
    return url_list

# Extract all school urls and store them along with their corresponding school udise code as key-value pairs
def main():
    global base_url
    final_dict = {}
    schools_done = 0
    state_urls = [base_url + "andhra-pradesh", base_url + "telangana"]
    if len(sys.argv) == 2:
        if sys.argv[1] == "AP":
            state_urls = [base_url + "andhra-pradesh"]
        elif sys.argv[1] == "TS":
            state_urls = [base_url + "telangana"]
    for state_url in state_urls:
        district_urls = get_table_urls(state_url)
        for district_url in district_urls:
            block_urls = get_table_urls(district_url)
            for block_url in block_urls:
                cluster_urls = get_table_urls(block_url)
                for cluster_url in cluster_urls:
                    school_urls = get_table_urls(cluster_url)
                    for school_url in school_urls:
                        url_parts = school_url.split('/')
                        if len(url_parts) < 2:
                            continue
                        final_dict[url_parts[-2]] = school_url
                        schools_done += 1
                        if schools_done % 200 == 0:
                            print(f'{schools_done} schools are done')
                time.sleep(4)
    # Storing dict in a pickle file
    with open('school_urls.pkl', 'wb') as f:
        print(len(final_dict))
        pickle.dump(final_dict, f)

if __name__ == '__main__':
	main()