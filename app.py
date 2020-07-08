
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
from os import getenv
from datetime import datetime
load_dotenv()

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipedb'
app.config['MONGO_URI'] = os.getenv(
    'MONGO_URI')

mongo = PyMongo(app)

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")
#print("now =", now)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/get_category')
def get_categories():
    categories_cursor = mongo.db.categories.find()
    return render_template("category.html", categories=categories_cursor)


@app.route('/recipe')
def get_recipe():
    recipe_cursor = mongo.db.recipe.find(
        {'title': 'werwe'})
    return render_template("recipe.html", recipe=recipe_cursor)


@app.route('/all')
def get_all():
    recipe_cursor = mongo.db.recipe.find()
    return render_template("all.html", recipe=recipe_cursor)


@app.route('/submit_recipe')
def submit_recipe():
    categories_cursor = mongo.db.categories.find()
    return render_template("submit_recipe.html", categories=categories_cursor)


@app.route('/send_recipe', methods=['POST'])
def send_recipe():
    recipe_cursor = mongo.db.recipe
    return_data = request.form.to_dict()
    return_data["date_added"] = dt_string
    print(return_data)
    recipe_cursor.insert_one(return_data)

    return redirect(url_for('submit_recipe'))


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")), debug=True)
