import time


def programLSIP():
    import json
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException



    with open('items_for_search.json', 'r') as file:
        items_data = json.load(file)

    print("lis_skins_item_parser\n")

    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=C:/Users/dimad/AppData/Local/Google/Chrome/User Data/")
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    browser.set_page_load_timeout(2)

    buy = False
    while not buy:
        for item in items_data:

            price_lis = None
            try:
                print("Переходим на ", item["URL"])
                browser.get(item["URL"])
            except TimeoutException:
                price_lis = float(browser.find_element(By.CLASS_NAME, 'min-price-value').text.split()[0])
                print("Цена на lis-skins: ", price_lis)


            price_steam = item["price_steam"]
            print("Начальная цена Steam: ", price_steam)

            if price_lis != None:
                if (price_lis < ((price_steam / 2) * 0.85)):
                    print(float(price_lis), ' < ', ((float(price_steam) / 2) * 0.85), " Профит епта\n")

                    browser.get(item["URL"])
                    browser.find_element(By.XPATH,
                                     "//div[@class='buy-now buy-now-button' and contains(text(), 'Купить сейчас')]").click()
                    try:
                        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "buy-now-popup-button")))
                        # browser.find_element(By.XPATH,"//div[@class='buy-now-popup-button buy-now-popup-bottom-button' and contains(., 'Оплатить')]").click()

                    finally:
                        print("Куплено (наверное)")
                        buy = True

                else:
                    print(float(price_lis), ' < ', ((float(price_steam) / 2) * 0.85), " Нихуя не профит ебать\n")

                time.sleep(1)

    browser.quit()

# programLSIP()