'''Данное приложение поможет Вам найти лучшие предложения с маркетплейсов'''

from models.offer import Offer
from services.marketplace import fetch_from_marketplace
from services.storage import load_offers, save_offer  # Исправленный импорт

def main():
    offers = load_offers()

    while True:
        print("Что сделать: 1 - показать предложения, 2 - выйти, 3 - добавить вручную, 4 - искать дешевле цены, 5 - найти на маркетплейсе, 6 - искать дороже цены, 7 - показать по источнику")
        try:
            requests = int(input("Введите запрос: "))
        except ValueError:
            print("Пожалуйста, введи число!")
            continue

        if requests == 1:
            offers.sort(key=lambda x: x.price)
            for i, offer in enumerate(offers, 1):
                print(f"{i}. {offer.get_details()}")
        elif requests == 2:
            print("Пока!")  # Больше не нужно сохранять весь список, SQLite делает это автоматически
            break
        elif requests == 3:
            name = input("Введи название товара: ")
            try:
                price = int(input("Введи цену товара: "))
            except ValueError:
                print("Цена должна быть числом!")
                continue
            link = input("Введи ссылку на товар: ")
            new_offer = Offer(name, price, link, source="Manual")
            save_offer(new_offer)  # Сохраняем одно предложение
            offers = load_offers()  # Обновляем список после добавления
            print("Товар добавлен!")
        elif requests == 4:
            try:
                max_price = int(input("Введите сумму, до которой будем искать: "))
            except ValueError:
                print("Сумма должна быть числом!")
                continue
            filtered_offers = [offer for offer in offers if offer.is_cheap(max_price)]
            filtered_offers.sort(key=lambda x: x.price)
            if filtered_offers:
                for i, offer in enumerate(filtered_offers, 1):
                    print(f"{i}. {offer.get_details()}")
            else:
                print("Нет товаров дешевле этой суммы!")
        elif requests == 5:
            query = input("Введи название товара для поиска на маркетплейсе: ")
            new_offer = fetch_from_marketplace(query)
            save_offer(new_offer)  # Сохраняем одно предложение
            offers = load_offers()  # Обновляем список
            print(f"Найдено и добавлено: {new_offer.get_details()}")
        elif requests == 6:
            try:
                min_price = int(input("Введите сумму, от которой будем искать: "))
            except ValueError:
                print("Сумма должна быть числом!")
                continue
            filtered_offers = [offer for offer in offers if offer.is_expensive(min_price)]
            filtered_offers.sort(key=lambda x: x.price)
            if filtered_offers:
                for i, offer in enumerate(filtered_offers, 1):
                    print(f"{i}. {offer.get_details()}")
            else:
                print("Нет товаров дороже этой суммы!")
        elif requests == 7:
            source = input("Введи источник (Manual/AliExpress): ")
            filtered_offers = [offer for offer in offers if offer.source == source]
            if filtered_offers:
                for i, offer in enumerate(filtered_offers, 1):
                    print(f"{i}. {offer.get_details()}")
            else:
                print("Товаров с таким источником нет!")
        else:
            print("Неверный ввод, попробуй еще раз!")

if __name__ == "__main__":
    main()