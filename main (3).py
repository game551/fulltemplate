import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Application, CallbackContext, JobQueue

# Configuration for the bot
TELEGRAM_TOKEN = '6317942460:AAEvXCCGsiwI6Dy5BuZK3TLy7Ok47NGXYbk'
CHAT_ID = '-1001963236331'

# List of products and price ranges
products = [
    {"name": "iphone", "min_price": 100, "max_price": 300},
    {"name": "macbook", "min_price": 500, "max_price": 1000}
]

def format_price(price_text):
    """Convert price from string to float, removing currency symbols and commas."""
    return float(price_text.replace('€', '').replace(',', '.').strip())

def fetch_ads(product, min_price, max_price):
    """Fetch ads from Wallapop based on product name and price range."""
    url = f"https://es.wallapop.com/search?kws={product}&minPrice={min_price}&maxPrice={max_price}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    ads = soup.find_all('div', class_='card-product')
    results = []
    for ad in ads:
        link = ad.find('a').get('href')
        price_text = ad.find('span', class_='product-info-price').text
        price = format_price(price_text)
        if min_price <= price <= max_price:
            results.append((link, price_text))
    return results

async def alert_ads(context: CallbackContext):
    """Check for new ads and send alerts."""
    for product in products:
        name = product['name']
        min_price = product['min_price']
        max_price = product['max_price']
        ads = fetch_ads(name, min_price, max_price)
        for link, price in ads:
            message = f'New ad for {name}: {price} at {link}'
            await context.bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    """Set up the Telegram bot and run it."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    jq: JobQueue = app.job_queue

    # Schedule to run the alert_ads function every hour
    jq.run_repeating(alert_ads, interval=600, first=0, chat_id=CHAT_ID)  # Checks every hour

    app.run_polling()

if __name__ == '__main__':
    main()
