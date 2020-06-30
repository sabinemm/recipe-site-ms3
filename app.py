
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
from os import getenv
load_dotenv()

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipedb'
app.config['MONGO_URI'] = os.getenv(
    'MONGO_URI')

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_category')
def get_categories():
    categories_cursor = mongo.db.categories.find()
    return render_template("category.html", categories=categories_cursor)


@app.route('/recipe')
def get_recipe():
    recipe_cursor = mongo.db.recipe.find()
    return render_template("recipe.html", recipe=recipe_cursor)


@app.route('/submit_recipe')
def add_recipe():
    return render_template("submit_recipe.html")


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")), debug=True)
