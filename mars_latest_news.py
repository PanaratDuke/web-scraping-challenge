from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time

executable_path = {'executable_path': 'chromedriver.exe'}
url = 'https://mars.nasa.gov/news'
with Browser('chrome', **executable_path, headless=False) as browser:
    browser.visit(url)
    time.sleep(3)
    html=browser.html

nasa_news= {}
top_article_title=""
top_article_body=""

soup = BeautifulSoup(html, 'html.parser')
titles = soup.find('div', class_="list_text")
top_article_title = titles.find('a')['href']
# top_article_title.a['href']
top_article_body = titles.find('div',class_="article_teaser_body").text

# for cur_div in titles.find_all('div'):

#     print(cur_div.attrs["class"])
#     if "content_title" in cur_div.attrs["class"]:
#         cur_a = cur_div.find('a')
#         top_article_title = cur_a.text
#         print(cur_a)
#         print(cur_div)
#     if "article_teaser_body" in cur_div.attrs["class"]:
#         top_article_body = cur_div.text

# traverse through the dictionary using [] and use = to set value as 
nasa_news[top_article_title] = top_article_body

print(nasa_news)
