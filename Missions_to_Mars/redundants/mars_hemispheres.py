from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

img_url = ""
title = ""
hemisphere_image_urls ={}

browser.visit(usgs_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')
titles = soup.find_all('div', class_="item")

for each_title in titles: 
    key_word = each_title.find('h3').text
    print(key_word)
#     browser.find_link_by_partial_text('Hemisphere Enhanced').click()
    browser.find_link_by_partial_text(key_word).click()
#     print(browser.url)
    # you can access the attribute using [href]
    img_url = browser.find_link_by_text('Sample').first['href']
#     hemisphere_image_urls.update({test.text:img_url})
    print(img_url)
    hemisphere_image_urls[key_word]=img_url
    browser.back()

    print(hemisphere_image_urls)