def programIDF():
    import re
    import json
    from selenium import webdriver



    print("item_id_finder\n")
    with open('items_for_search.json', 'r') as file:
        items_data = json.load(file)

    browser = webdriver.Chrome()

    for item in items_data:
        if item["item_id"] == '' or item["item_id"] == 0 or item["item_id"] == "":

            steam_link = item["SteamURL"]
            steam_link = steam_link.replace('в„ў', '%E2%84%A2')
            browser.get(steam_link)

            full_page_content = browser.page_source
            # print(full_page_content)

            result = re.findall(r'Market_LoadOrderSpread\(\s*(\d+)\s*\)', str(full_page_content))
            item["item_id"] = result[0]

    with open('items_for_search.json', 'w') as file:
        json.dump(items_data, file, indent=2)

# programIDF()