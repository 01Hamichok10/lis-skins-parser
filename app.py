import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("Загружаем информацию из JSON...\n")
with open('items_for_search.json', 'r') as file:
    items_data = json.load(file)


options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:/Users/dimad/AppData/Local/Google/Chrome/User Data/")
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

#cookies = open("cookies")

# if cookies is not None:
#     print("Куки найдены, загружаем...")
#     browser.get("https://lis-skins.ru")
#     for cookie in pickle.load(open("cookies", "rb")):
#         browser.add_cookie(cookie)
#         print("Загружаем: ", cookie)
# else:
#     print("Куки не найдены, войдите в аккаунт")
#     browser.get("https://lis-skins.ru")
#     browser.find_element(By.XPATH, '/html/body/header/section/div/div[2]/div/a').click()
#     time.sleep(10)
#
#     pickle.dump(browser.get_cookies(), open("cookies", "wb"))



for item in items_data:
    browser.get(item["URL"])

    price_lis = browser.find_element(By.CLASS_NAME, 'min-price-value').text.split()[0]
    print("Цена на lis-skins: ",price_lis)

    # Извлекаем значение атрибута "data-href" из элемента
    steam_link = browser.find_element(By.CLASS_NAME, 'steam-price-title').get_attribute('data-href')
    print("Переходим в Steam - ", steam_link)

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
        browser.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]').click()
        time.sleep(3)

    else:
        print(float(price_lis), ' < ', ((float(price_steam) / 2) * 0.85), " Нихуя не профит ебать\n")

        browser.get(item["URL"])
        browser.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]').click()

