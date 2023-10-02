import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import subprocess
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/get_gifts")
def get_gifts():
    gifts = list(mongo.db.gifts.find())
    return render_template("allgifts.html", gifts=gifts)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    gifts = list(mongo.db.gifts.find({"$text": {"$search": query}}))
    return render_template("allgifts.html", gifts=gifts)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

# put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
        flash("You have been logged out")
    return redirect(url_for("login"))


@ app.route("/add_gift", methods=["GET", "POST"])
def add_gift():
    if request.method == "POST":
        gift = {
            "list_name": request.form.get("list_name"),
            "gift_item": request.form.get("gift_item"),
            "cost": request.form.get("cost"),
            "where_to_buy": request.form.get("where_to_buy"),
            "link": request.form.get("link"),
            "created_by": session["user"]
        }
        mongo.db.gifts.insert_one(gift)
        flash("Gift Successfully Added")
        return redirect(url_for("get_gifts"))

    gifts = mongo.db.gifts.find().sort("list_name", 1)
    return render_template("add_gift.html", gifts=gifts)


@app.route("/edit_gift/<gift_id>", methods=["GET", "POST"])
def edit_gift(gift_id):
    if request.method == "POST":
        submit = {
                "list_name": request.form.get("list_name"),
                "gift_item": request.form.get("gift_item"),
                "cost": request.form.get("cost"),
                "where_to_buy": request.form.get("where_to_buy"),
                "link": request.form.get("link"),
                "created_by": session["user"]
            }

        mongo.db.gifts.update({"_id": ObjectId(gift_id)}, submit)
        flash("Gift Successfully Updated")
        
    gift_item = mongo.db.gifts.find_one({"_id": ObjectId(gift_id)})
    gifts = mongo.db.gifts.find().sort("list_name", 1)
    return render_template("edit_gift.html", gifts=gifts, gift_item=gift_item)


@app.route("/delete_gift/<gift_id>")
def delete_gift(gift_id):
    mongo.db.gifts.remove({"_id": ObjectId(gift_id)})
    flash("Gift Successfully Deleted")
    return redirect(url_for("get_gifts"))


@app.route('/update_running_total', methods=['GET'])
def update_running_total():
    # Run the dashboard.py script as a subprocess
    subprocess.call(["python", "dashboard.py"])
    return "Running total updated successfully."


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
