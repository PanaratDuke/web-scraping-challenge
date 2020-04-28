from bs4 import BeautifulSoup
import requests
import os
from splinter import Browser
import time

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

mars_weather = ""
twitter_url = 'https://twitter.com/marswxreport?lang=en'


browser.visit(twitter_url)
time.sleep(3)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

extract_mars_weather = soup.find_all('div', attrs={'data-testid': 'tweet'})
for each_weather in extract_mars_weather: 
    mars_weather_info = each_weather.find_all('span')[4].text
#     print(mars_weather)
    break

mars_weather = {"mars_weather":mars_weather_info}
print(mars_weather)