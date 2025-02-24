class Offer:
    def __init__(self, name, price, link, source="Manual", id=None):
        self.id = id  # Добавляем id, может быть None для новых объектов
        self.name = name
        self.price = float(price)
        self.link = link
        self.source = source

    def display(self):
        return f"{self.name} - {self.price} руб. - {self.link}"

    def is_cheap(self, max_price):
        return self.price <= max_price

    def is_expensive(self, min_price):
        return self.price >= min_price

    def get_details(self):
        return f"Товар: {self.name}, Цена: {self.price} руб., Ссылка: {self.link}, Источник: {self.source}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "link": self.link,
            "source": self.source
        }