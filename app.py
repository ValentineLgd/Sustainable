import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
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


@app.route("/add_brands", methods=["GET", "POST"])
def add_brands():
    if request.method == "POST":
        brand = {
            "country": request.form.get("country"),
            "brand_name": request.form.get("brand_name"),
            "description": request.form.get("description"),
            "website": request.form.get("website"),
        }
        mongo.db.brands.insert_one(brand)
        flash("Brand Successfully Added")
        return redirect(url_for("get_brands"))
    return render_template("add_brands.html")


@app.route("/edit_brands/<brand_id>", methods=["GET", "POST"])
def edit_brands(brand_id):
    if request.method == "POST":
        submit = {
            "country": request.form.get("country"),
            "brand_name": request.form.get("brand_name"),
            "description": request.form.get("description"),
            "website": request.form.get("website"),
        }
        mongo.db.brands.update({"_id": ObjectId(brand_id)}, submit)
        flash("Brand Successfully Updated")
        return redirect(url_for("manage_brands"))

    brand = mongo.db.brands.find_one({"_id": ObjectId(brand_id)})
    return render_template("edit_brands.html", brand=brand)



@app.route("/delete_brand/<brand_id>")
def delete_brand(brand_id):
    mongo.db.brands.remove({"_id": ObjectId(brand_id)})
    flash("Brand Successfully Deleted")
    return redirect(url_for("get_brands"))


@app.route("/manage_brands")
def manage_brands():
    brands = mongo.db.brands.find()
    return render_template("manage_brands.html", brands=brands)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)