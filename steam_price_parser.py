def programSPP():
    import json
    import time
    from selenium import webdriver
    from bs4 import BeautifulSoup as BS

    browser = webdriver.Chrome()

    print("steam_price_parser\n")
    with open('items_for_search.json', 'r') as file:
        items_data = json.load(file)

    # Условие НТ сделать надо блять
    end = False
    while end == False:
        for item in items_data:

            browser.get(item["SteamURL"])
            time.sleep(1)
            browser.execute_script("window.open('', '_blank');")
            browser.switch_to.window(browser.window_handles[1])
            time.sleep(0.5)

            browser.get("https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=1&item_nameid=" + item["item_id"] + "&two_factor=0")
            print("Пробуем: https://steamcommunity.com/market/itemordershistogram?country=RU&language=russian&currency=1&item_nameid=" + item["item_id"] + "&two_factor=0")

            soup = BS(browser.page_source, 'html.parser')
            print(browser.page_source)
            pre_tag = soup.find('pre')
            if pre_tag:
                # Получаем текст из тега <pre>
                json_text = pre_tag.text

                # Разбираем JSON данные
                try:
                    json_data = json.loads(json_text)
                    print(json_data)
                    item["price_steam"] = json_data.get("buy_order_graph")[0][0]
                except json.JSONDecodeError as e:
                    print(f"Ошибка при разборе JSON: {e}")
            else:
                print("Тег <pre> не найден на странице.")

            browser.close()
            browser.switch_to.window(browser.window_handles[0])

            time.sleep(5)

        with open('items_for_search.json', 'w') as file:
            json.dump(items_data, file, indent=2)

        time.sleep(15)
        # end = True
        # browser.close()

# programSPP()