#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# -------------------------------
# ROUTES
# -------------------------------

@app.get('/')
def index():
    return "<h1>Bakery API</h1>"


# 1) GET /bakeries
@app.get('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()
    response = [
        bakery.to_dict(only=(
            'id', 'name', 'created_at', 'updated_at', 'baked_goods'
        ))
        for bakery in bakeries
    ]
    return jsonify(response), 200


# 2) GET /bakeries/<id>
@app.get('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)

    if bakery is None:
        return jsonify({"error": "Bakery not found"}), 404

    return jsonify(
        bakery.to_dict(only=(
            'id', 'name', 'created_at', 'updated_at', 'baked_goods'
        ))
    ), 200


# 3) GET /baked_goods/by_price
@app.get('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = [
        g.to_dict(only=(
            'id', 'name', 'price', 'created_at', 'updated_at',
            'bakery', 'bakery_id'
        ))
        for g in goods
    ]
    return jsonify(response), 200


# 4) GET /baked_goods/most_expensive
@app.get('/baked_goods/most_expensive')
def most_expensive():
    item = BakedGood.query.order_by(BakedGood.price.desc()).first()

    if item is None:
        return jsonify({"error": "No baked goods found"}), 404

    return jsonify(
        item.to_dict(only=(
            'id', 'name', 'price', 'created_at', 'updated_at',
            'bakery', 'bakery_id'
        ))
    ), 200


# -------------------------------
# MAIN
# -------------------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
