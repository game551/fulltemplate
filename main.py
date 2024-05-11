import time

import requests
from keepAlive import keep_alive

keep_alive()

bot_token = "5995500060:AAFNS4pL8XeDWCpKOqS0t_SJyumASnhqIi8"
bot_chat_id = "-1001585615298"


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chat_id + '&parse_mode=Markdown&text=' + bot_message
    res = requests.get(send_text)
    
    return True


def get_file_data(file):
    with open(file) as f:
        data = f.read().strip()
        my_file_data = data.split('\n')

    return my_file_data


def update_data(file, data):
    with open(file, "a") as f:
        f.write(data + '\n')


def wall_pop_search(search_term):
    keyword = search_term.split("|")[0]
    min_price = search_term.split("|")[1]
    max_price = search_term.split("|")[2]
  
    wallapop_api_url = f"https://api.wallapop.com/api/v3/general/search?min_sale_price={min_price}&max_sale_price={max_price}&latitude=40.41956&longitude=-3.69196&time_filter=today&keywords={keyword}&filters_source=default_filters&order_by=newest"
    response = requests.get(wallapop_api_url)
    data = response.json()["search_objects"]
    for single in data:
        already_done = get_file_data("Already Done.txt")
        product_id = single["id"]
        if product_id not in already_done:
            title = single["title"]
            price = single["price"]
            description = str(single["description"]).replace("\r", " ").replace("\n", " ")
            url = "https://uk.wallapop.com/item/" + single["web_slug"]
            print(f"{title} - {price} - {url}")
            alert_message = f"Title: {title}\n\nDescription: {description}\nUrl: {url} \n\nPrice: {price}"
            telegram_bot_sendtext(alert_message)
            update_data("Already Done.txt", product_id)


keywords_list = get_file_data("keywords.txt")
while True:

    for keyword in keywords_list:
        wall_pop_search(keyword)
    print("waiting for 10 Seconds")
    time.sleep(10)
