import json
import requests
from bs4 import BeautifulSoup as BS

print("Загружаем информацию из JSON...\n")
with open('items_for_search.json', 'r') as file:
    items_data = json.load(file)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

for item in items_data:

    response_lis = requests.get(item["URL"], headers=headers)

    souplis = BS(response_lis.text, 'html.parser')
    print(souplis.find('h1').get_text(strip=True))

    min_price_lis = souplis.find('div', class_='min-price-value').find(string=True).strip()
    print("Min Price:", min_price_lis)

    steam_link = souplis.find('a', class_='steam-price-title')['data-href']

    steam_GET = "https://steamcommunity.com/market/priceoverview/?market_hash_name=" + steam_link.split("/")[-1] + "&appid=730&currency=5/"
    response_steam = requests.get(steam_GET, headers=headers)
    soupsteam = BS(response_steam.text, 'html.parser')

    price_steam = response_steam.json().get('lowest_price')[:-5].replace(",",".")

    print("Начальная цена Steam:", price_steam)

    if (float(price_steam)/float(min_price_lis) >= 2):
        print("Разница: ", float(price_steam)/float(min_price_lis), " Профит епта\n")

    else:
        print("Разница: ", float(price_steam)/float(min_price_lis), " Нихуя не профит ебать\n")