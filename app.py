# Code adapted from Code Institute Mini-Project : Putting it all together #

import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/get_brands")
def get_brands():
    brands = mongo.db.brands.find()
    return render_template("get_brands.html", brands=brands)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    brands = list(mongo.db.brands.find({"$text": {"$search": query}}))
    return render_template("get_brands.html", brands=brands)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}!".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "manage_brands"))
            else:
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/manage_brands")
def manage_brands():
    brands = mongo.db.brands.find()
    return render_template("manage_brands.html", brands=brands)


@app.route("/add_brands", methods=["GET", "POST"])
def add_brands():
    if request.method == "POST":
        brand = {
            "country": request.form.get("country"),
            "brand_name": request.form.get("brand_name"),
            "category_name": request.form.get("category_name"),
            "description": request.form.get("description"),
            "website": request.form.get("website"),
            "created_by": session["user"]
        }
        mongo.db.brands.insert_one(brand)
        flash("Brand Successfully Added! Thank you for your help!")
        return redirect(url_for("manage_brands"))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_brands.html", categories=categories)


@app.route("/edit_brands/<brand_id>", methods=["GET", "POST"])
def edit_brands(brand_id):
    if request.method == "POST":
        submit = {
            "country": request.form.get("country"),
            "brand_name": request.form.get("brand_name"),
            "category_name": request.form.get("category_name"),
            "description": request.form.get("description"),
            "website": request.form.get("website"),
            "created_by": session["user"]
        }
        mongo.db.brands.update({"_id": ObjectId(brand_id)}, submit)
        flash("Brand Successfully Updated! Thank you for your help!")
        return redirect(url_for("manage_brands"))

    brand = mongo.db.brands.find_one({"_id": ObjectId(brand_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("edit_brands.html", brand=brand, categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists : please try again ")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful! Welcome, {}!".format(
                            request.form.get("username")))
        return redirect(url_for("manage_brands"))

    return render_template("register.html")


@app.route("/delete_brand/<brand_id>")
def delete_brand(brand_id):
    mongo.db.brands.remove({"_id": ObjectId(brand_id)})
    flash("Brand Successfully Deleted")
    return redirect(url_for("manage_brands"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)