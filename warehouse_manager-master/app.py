

import os
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

# =========================================================
# Flask App
# =========================================================
app = Flask(__name__)

# =========================================================
# MongoDB Connection (NO flask-pymongo)
# =========================================================
MONGO_URI = "mongodb+srv://db_user:hadirchamta@cluster0.cf0lyt3.mongodb.net/shop_inventory"
client = MongoClient(MONGO_URI)

db = client.shop_inventory
products_col = db.products
categories_col = db.categories
manufacturers_col = db.manufacturers
suppliers_col = db.suppliers

# =========================================================
# DASHBOARD
# =========================================================
@app.route('/')
@app.route('/get_dashboard')
def get_dashboard():
    products = list(products_col.find())
    return render_template(
        'dashboard.html',
        bar_name="Products",
        bar_quantity=products,
        bar_colour=products,
        bar_product=products,
        doughnut_name="Categories",
        doughnut_quantity=products,
        doughnut_colour=products,
        doughnut_category=products
    )

# =========================================================
# PRODUCTS
# =========================================================
@app.route('/get_products')
def get_products():
    return render_template(
        'products.html',
        products=products_col.find()
    )

@app.route('/search_products', methods=['POST'])
def search_products():
    search_input = request.form['input_search']
    words = search_input.split()

    query = {
        "$or": [
            {"product_name": {"$regex": word, "$options": "i"}}
            for word in words
        ]
    }

    results = list(products_col.find(query))

    if results:
        return render_template(
            'searchresults.html',
            search_text=search_input,
            results=results
        )
    return redirect(url_for('search_empty'))

@app.route('/search_empty')
def search_empty():
    return render_template('searchnull.html')

@app.route('/add_product')
def add_product():
    return render_template(
        'addproduct.html',
        manufacturers=manufacturers_col.find(),
        categories=categories_col.find(),
        suppliers=suppliers_col.find()
    )

@app.route('/insert_product', methods=['POST'])
def insert_product():
    products_col.insert_one(dict(request.form))
    return redirect(url_for('get_products'))

@app.route('/edit_product/<product_id>')
def edit_product(product_id):
    product = products_col.find_one({'_id': ObjectId(product_id)})
    return render_template(
        'editproduct.html',
        product=product,
        manufacturers=manufacturers_col.find(),
        categories=categories_col.find(),
        suppliers=suppliers_col.find()
    )

@app.route('/update_product/<product_id>', methods=['POST'])
def update_product(product_id):
    products_col.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': dict(request.form)}
    )
    return redirect(url_for('get_products'))

@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    products_col.delete_one({'_id': ObjectId(product_id)})
    return redirect(url_for('get_products'))

# =========================================================
# CATEGORIES
# =========================================================
@app.route('/get_categories')
def get_categories():
    return render_template(
        'categories.html',
        categories=categories_col.find()
    )

@app.route('/add_category')
def add_category():
    return render_template(
        'addcategory.html',
        categories=categories_col.find()
    )

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories_col.insert_one(dict(request.form))
    return redirect(url_for('get_categories'))

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    category = categories_col.find_one({'_id': ObjectId(category_id)})
    return render_template(
        'editcategory.html',
        category=category
    )

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    categories_col.update_one(
        {'_id': ObjectId(category_id)},
        {'$set': dict(request.form)}
    )
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>', methods=['POST'])
def delete_category(category_id):
    categories_col.delete_one({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

# =========================================================
# RUN APP
# =========================================================
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)