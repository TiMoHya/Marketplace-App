
from models.offer import Offer
import requests
import hashlib
import time
from models.offer import Offer

# Твои будущие ключи (замени, когда получишь)
APP_KEY = "YOUR_APP_KEY"
APP_SECRET = "YOUR_APP_SECRET"


def generate_sign(params, secret):
    """Генерирует подпись для API AliExpress."""
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f"{k}{v}" for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode()).hexdigest().upper()


def fetch_from_marketplace(query):
    """Получает данные о товаре с AliExpress (пока заглушка)."""
    # Параметры для будущего реального запроса
    url = "http://gw.api.taobao.com/router/rest"
    params = {
        "method": "aliexpress.affiliate.product.query",
        "app_key": APP_KEY,
        "sign_method": "md5",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "v": "2.0",
        "format": "json",
        "keywords": query,
        "page_no": "1",
        "page_size": "1",
    }
    params["sign"] = generate_sign(params, APP_SECRET)

    # Пока нет ключей — имитация ответа
    try:
        # Раскомментируй это, когда будут ключи
        # response = requests.get(url, params=params)
        # if response.status_code == 200:
        #     data = response.json()
        #     product = data["aliexpress_affiliate_product_query_response"]["resp_result"]["result"]["products"][0]
        #     return Offer(product["product_title"], float(product["target_sale_price"]), product["product_detail_url"])

        # Заглушка для теста
        fake_response = {
            "product_title": f"{query} (AliExpress)",
            "target_sale_price": "5000",  # Пример цены
            "product_detail_url": f"https://aliexpress.com/item/{query}"
        }
        return Offer(fake_response["product_title"], float(fake_response["target_sale_price"]),
                     fake_response["product_detail_url"], source="AliExpress")
    except Exception as e:
        return Offer(query, 9999, f"Ошибка: {str(e)}")