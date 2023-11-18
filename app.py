import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



print("Загружаем информацию из JSON...\n")
with open('items_for_search.json', 'r') as file:
    items_data = json.load(file)

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/dimad/AppData/Local/Google/Chrome/User Data/")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

buy = False
while buy == False:
    for item in items_data:
        print("Переходим на ", item["URL"])
        browser.get(item["URL"])

        price_lis = browser.find_element(By.CLASS_NAME, 'min-price-value').text.split()[0]
        print("Цена на lis-skins: ", price_lis)

        # Извлекаем значение атрибута "data-href" из элемента
        steam_link = browser.find_element(By.CLASS_NAME, 'steam-price-title').get_attribute('data-href')
        print("Получаем ссылку Steam - ", steam_link)

        steam_GET = "https://steamcommunity.com/market/priceoverview/?market_hash_name=" + steam_link.split("/")[-1] + "&appid=730&currency=5/"
        print("Создаем запрос в Steam: ", steam_GET)
        browser.get(steam_GET)

        steam_response = browser.find_element(By.TAG_NAME, 'pre').text
        steam_data = json.loads(steam_response)
        price_steam = steam_data['lowest_price'].replace(' pуб.', '').replace(',', '.')
        print("Начальная цена Steam: ", price_steam)

        if (float(price_lis) < ((float(price_steam) / 2) * 0.85)):
            print(float(price_lis), ' < ', ((float(price_steam) / 2) * 0.85), " Профит епта\n")

            browser.get(item["URL"])
            browser.find_element(By.XPATH,
                             "//div[@class='buy-now buy-now-button' and contains(text(), 'Купить сейчас')]").click()
            try:
                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "buy-now-popup-button")))
                browser.find_element(By.XPATH,"//div[@class='buy-now-popup-button buy-now-popup-bottom-button' and contains(., 'Оплатить')]").click()

            finally:
                print("Куплено (наверное)")
                buy = True

        else:
            print(float(price_lis), ' < ', ((float(price_steam) / 2) * 0.85), " Нихуя не профит ебать\n")

browser.quit()