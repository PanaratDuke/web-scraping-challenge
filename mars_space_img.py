from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

browser.visit(jpl_url)
time.sleep(3)

feat_img_url = "" 
feat_img_url_1 = ""
feat_img_url_2 = "" #Using This one to retrieve url
feat_img_url_new = ""

feat_img_dict = {}

html = browser.html
soup = BeautifulSoup(html, 'lxml')

find_div_1 = soup.find('div', class_="jpl_logo")
feat_img_url_1 = find_div_1.a['href']

feat_img_url_1='http:'+feat_img_url_1
find_div_raw = soup.find('li', class_="slide")
feat_img_url = find_div_raw.a['data-fancybox-href']
feat_img_url_2=feat_img_url_1+feat_img_url[1:]

feat_img_dict['feat_img'] = feat_img_url_2

print(feat_img_dict)
