'''Данное приложение поможет Вам найти лучшие предложения с маркетплейсов'''

from flask import Flask, render_template, request, redirect, url_for
from models.offer import Offer
from services.marketplace import fetch_from_marketplace
from services.storage import load_offers, save_offer, delete_offer  # Добавляем delete_offer

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    offers = load_offers()
    offers.sort(key=lambda x: x.price)

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'add':
            name = request.form['name']
            try:
                price = float(request.form['price'])
            except ValueError:
                return "Цена должна быть числом!", 400
            link = request.form['link']
            new_offer = Offer(name, price, link, source="Manual")
            save_offer(new_offer)

        elif action == 'search':
            query = request.form['query']
            new_offer = fetch_from_marketplace(query)
            save_offer(new_offer)

        elif action == 'filter':
            try:
                price = float(request.form['price'])
            except ValueError:
                return "Цена должна быть числом!", 400
            filter_type = request.form['filter_type']
            if filter_type == "cheap":
                offers = [o for o in offers if o.is_cheap(price)]
            else:
                offers = [o for o in offers if o.is_expensive(price)]
            offers.sort(key=lambda x: x.price)

    return render_template('index.html', offers=offers)

@app.route('/delete/<int:offer_id>', methods=['POST'])
def delete(offer_id):
    delete_offer(offer_id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)