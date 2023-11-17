import json
import requests
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import undetected_chromedriver
import time
import logging

options = webdriver.ChromeOptions()
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0")
options.add_argument("--disable-blink-features=AutomationControlled")
# Указание уровня логирования для ChromeDriver (можете выбрать другой уровень по необходимости)
logging.basicConfig(level=logging.INFO)
service_log_path = "./chromedriver.log"
service_args = ['--verbose']
options.add_argument('--headless')  # Опционально, если вы хотите, чтобы браузер работал в фоновом режиме


driver = webdriver.Chrome(options=options, service_args=service_args)


print("Загружаем информацию из JSON...\n")
with open('items_for_search.json', 'r') as file:
    items_data = json.load(file)

for item in items_data:

    driver.get(["URL"])
    time.sleep(15)
    response_lis = requests.get(item["URL"])

    souplis = BS(response_lis.text, 'html.parser')
    print(souplis.find('h1').get_text(strip=True))


    min_price_lis = souplis.find('div', class_='min-price-value').find(string=True).strip()
    print("Min Price:", min_price_lis)

    steam_link = souplis.find('a', class_='steam-price-title')['data-href']

    steam_GET = "https://steamcommunity.com/market/priceoverview/?market_hash_name=" + steam_link.split("/")[-1] + "&appid=730&currency=5/"
    response_steam = requests.get(steam_GET)
    soupsteam = BS(response_steam.text, 'html.parser')

    price_steam = response_steam.json().get('lowest_price')[:-5].replace(",",".")

    print("Начальная цена Steam:", price_steam)

    if (float(min_price_lis) < ((float(price_steam)/2)*0.85)):
        print(float(min_price_lis), ' < ', ((float(price_steam)/2)*0.85), " Профит епта\n")

    else:
        print(float(min_price_lis), ' < ', ((float(price_steam)/2)*0.85),  " Нихуя не профит ебать\n")