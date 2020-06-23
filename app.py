
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
from os import getenv

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipedb'
app.config['MONGO_URI'] = os.getenv(
    'MONGO_URI')


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_category')
def get_categories():
    #    categories = mongo.db.categories.find()
    #    print(categories)
    return render_template("category.html")  # categories=categories)


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")), debug=True)
