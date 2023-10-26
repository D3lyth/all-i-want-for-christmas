import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from functools import wraps
from countdown import christmas_countdown
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# @login_required decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # no "user" in session
        if "user" not in session:
            flash("You must log in to view this page")
            return redirect(url_for("login"))
        # user is in session
        return f(*args, **kwargs)
    return decorated_function


@app.route("/")
def welcome():
    return render_template("welcome.html")

# Login decorator


@app.route("/profile_login", methods=["GET", "POST"])
def profile_login():
    if "user" not in session:
        # only if there isn't a current session["user"]
        if request.method == "POST":
            # check if username exists in db
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})

            if existing_user:
                # ensure hashed password matches user input
                if check_password_hash(
                        existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
                else:
                    # invalid password match
                    flash("Incorrect Username and/or Password")
                    return redirect(url_for("profile_login"))

            else:
                # username doesn't exist
                flash("Incorrect Username and/or Password")
                return redirect(url_for("profile_login"))

        return render_template("profile_login.html")

    # user is already logged-in, direct them to their profile
    return redirect(url_for("profile", username=session["user"]))

# Get Gifts decorator - to show all gifts


@app.route("/get_gifts")
@login_required
def get_gifts():
    user = session["user"]
    gifts = list(mongo.db.gifts.find({"created_by": user}))
    return render_template("allgifts.html", gifts=gifts)


# Search decorator for search bar


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    user = session["user"]
    gifts = list(mongo.db.gifts.find({"$text": {"$search": query}}))
    return render_template("allgifts.html", gifts=gifts)


# Register new user decorator

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
@login_required
def profile(username):
    # grab only the session["user"] profile
    if session["user"].lower() == username.lower():
        # find the session["user"] record
        user = mongo.db.users.find_one({"username": username})
        # grab only the gifts by this session["user"]
        gifts = list(mongo.db.gifts.find({"created_by": username}))
        return render_template("profile.html", user=user, gifts=gifts)

        # Calculate the countdown values
        countdown_values = christmas_countdown()

    # take the incorrect user to their own profile
    return redirect(url_for("welcome", username=session["user"]))


@app.route("/profile_logout")
@login_required
def profile_logout():
    if "user" in session:
        session.pop("user")  # Remove the user from the session
        flash("You have been logged out")
    else:
        # Handle the case when the user is not in the session
        flash("You are not logged in")
    return redirect(url_for("welcome"))


@ app.route("/add_gift", methods=["GET", "POST"])
@login_required
def add_gift():
    if request.method == "POST":
        gift_to_add = {
            "list_name": request.form.get("list_name"),
            "gift_item": request.form.get("gift_item"),
            "cost": request.form.get("cost"),
            "where_to_buy": request.form.get("where_to_buy"),
            "link": request.form.get("link"),
            "created_by": session["user"]
        }
        mongo.db.gifts.insert_one(gift_to_add)
        flash("Gift Successfully Added")
        return redirect(url_for("get_gifts"))

    gifts = mongo.db.gifts.find().sort("list_name", 1)
    return render_template("add_gift.html", gifts=gifts)


@app.route("/edit_gift/<gift_id>", methods=["GET", "POST"])
@login_required
def edit_gift(gift_id):
    # Find the gift, limiting to gifts created_by the current user
    gift_to_edit = mongo.db.gifts.find_one(
        {"_id": ObjectId(gift_id), "created_by": session["user"]})

    if gift_to_edit:
        if request.method == "POST":
            # Update the gift details based on the form input
            updated_gift = {
                "list_name": request.form.get("list_name"),
                "cost": request.form.get("cost"),
            }
            # Update the gift in the database
            mongo.db.gifts.update_one({"_id": ObjectId(gift_id)}, {
                                      "$set": updated_gift})
            # Redirect to the view of the updated gift
            return redirect(url_for("get_gifts"))
        else:
            # Render the edit page with the existing gift details
            return render_template("edit_gift.html", gift_item=gift_to_edit)

    else:
        # No gift found for the current user, send an error
        flash("Gift not found or you don't have permission to edit it")
        return redirect(url_for("get_gifts"))


@app.route("/delete_gift/<gift_id>")
@login_required
def delete_gift(gift_id):
    # find the gift
    gift_to_delete = mongo.db.gifts.find_one({"_id": ObjectId(gift_id)})

    if session["user"].lower() == gift_to_delete["created_by"].lower():
        # The session["user"] is the user who created this gift
        mongo.db.gifts.delete_one({"_id": ObjectId(gift_id)})
        flash("Gift Successfully Deleted")
    else:
        # Not the correct user to delete this gift
        flash("You don't have access to delete this gift")

    return redirect(url_for("get_gifts"))


@app.route("/mark_as_bought/<gift_id>")
@login_required
def mark_as_bought(gift_id):
    # Find the gift, ensuring it was created by the current user
    gift = mongo.db.gifts.find_one(
        {"_id": ObjectId(gift_id), "created_by": session["user"]})

    if gift:
        # Update the 'bought' field to True
        mongo.db.gifts.update_one({"_id": ObjectId(gift_id)}, {
                                  "$set": {"bought": True}})
        flash("Item marked as bought")

    return redirect(url_for("get_gifts"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
