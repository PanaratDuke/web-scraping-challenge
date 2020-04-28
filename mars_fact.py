from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import pandas as pd


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://space-facts.com/mars/'

mars_facts = ""
info_dict={}

tables = pd.read_html(url)
type(tables)

target_table=tables[0]

for each_row in target_table.index:
    each_row_df=target_table.loc[each_row]
    info_dict[each_row_df[0]]=each_row_df[1]

print(info_dict)
