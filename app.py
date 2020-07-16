
import os
from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
from os import getenv
from functools import wraps
from datetime import datetime
#from werkzeug.security import generate_password_hash, check_password_hash
load_dotenv()

# ---- CONFIG ----- #

app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.getenv(
    'MONGO_DBNAME')
app.config['MONGO_URI'] = os.getenv(
    'MONGO_URI')
app.config['SECRET_KEY'] = os.getenv(
    'SECRET_KEY')
mongo = PyMongo(app)

# ---- VARIABLES ----- #

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M")
users_collection = mongo.db.users

# ---- USER ----- #


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
@login_required
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid username or password. Please try again!'
        else:
            session['logged_in'] = True
            flash('You were just logged in')
            return redirect(url_for('welcome'))
    return render_template("users/login.html", error=error)


@app.route('/welcome')
def welcome():
    return render_template("users/welcome.html")


@ app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect(url_for('index'))


@app.route('/register')
def register():
    return render_template("register.html")

# ---- RECIPE PAGES ----- #


@app.route('/recipes/<category>')
def get_all(category):
    if category == "all":
        category = "All recipes"
        recipe = mongo.db.recipe.find()
    elif category == "other":
        recipe = mongo.db.recipe.find({"category_name": "Other"})
    else:
        recipe = mongo.db.recipe.find({"$text": {"$search": category}})
    return render_template("recipes.html", recipe=recipe, page_title=category)


@ app.route('/recipe/<recipe_id>')
def get_recipe(recipe_id):
    recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe.html", recipe=recipe)


@ app.route('/add_recipe')
def add_recipe():
    categories = mongo.db.categories.find()
    return render_template("recipe_form.html", categories=categories, the_recipe={}, page_title="Add Recipe")


@ app.route('/send_recipe', methods=['POST'])
def send_recipe():
    recipe = mongo.db.recipe
    return_data = request.form.to_dict()
    return_data["date_added"] = dt_string
    recipe.insert_one(return_data)
    return redirect(url_for('thank_you'))


@ app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")


@ app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    categories_cursor = mongo.db.categories.find()
    return render_template('edit_recipe.html', the_recipe=the_recipe, categories=categories_cursor)


@ app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    the_recipe = mongo.db.recipe.delete_one({"_id": ObjectId(recipe_id)})
    return render_template('index.html', the_recipe=the_recipe)


@ app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe = mongo.db.recipe
    categories_cursor = mongo.db.categories.find()
    recipe.update_one({"_id": ObjectId(recipe_id)},
                      {'$set': {
                          'title': request.form.get('title'),
                          'category_name': request.form.get('category_name'),
                          'description': request.form.get('description'),
                          'image_url': request.form.get('image_url'),
                          'ingredients': request.form.get('ingredients'),
                          'serves': request.form.get('serves'),
                          'prep': request.form.get('prep'),
                          'cooks': request.form.get('cooks'),
                          'difficulty': request.form.get('difficulty'),
                          'instructions': request.form.get('instructions'),
                          'tips': request.form.get('tips'),
                      }})

    return redirect(url_for('thank_you'))


@ app.route('/shop')
def shop():
    return render_template("shop.html")


@ app.route('/sub', methods=['POST'])
def sub():
    sub = mongo.db.subscribers
    return_data = request.form.to_dict()
    sub.insert_one(return_data)
    flash("Sucessfully Subscribed")
    return redirect(request.referrer)

# ---- SEARCH ----- #


@ app.route('/search', methods=["GET", "POST"])
def search():
    mongo.db.recipe.create_index([('$**', 'text')])
    query = request.form.get("query")
    result = mongo.db.recipe.find({"$text": {"$search": query}}).limit(10)
    result_num = mongo.db.recipe.find({"$text": {"$search": query}}).count()
    if result_num > 0:
        return render_template("search_results.html", result=result, query=query)
    else:
        return render_template("search_results.html", result=result, query=query, message="No results found. Please try again")

# ---- ERRORS ----- #


@ app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404


@ app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")), debug=True)
