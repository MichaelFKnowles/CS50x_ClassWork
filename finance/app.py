import os
import math

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    data = db.execute(
        "SELECT DISTINCT wallet.symbol, wallet.quantity, users.cash FROM users JOIN wallet ON users.id = wallet.user_id JOIN transactions ON wallet.user_id = transactions.user_id WHERE users.id = ? AND wallet.quantity IS NOT '0' ORDER BY wallet.symbol ASC",
        session["user_id"],
    )
    # print(data)
    stockVal = 0
    if data:
        cash = math.floor(data[0]["cash"] * 100) / 100
        print("******** cash: ", cash)
        for row in data:
            price = lookup(row["symbol"])
            row["current_price_per_share"] = price["price"]
            row["current_value"] = price["price"] * row["quantity"]
            stockVal += price["price"] * row["quantity"]
        data[0]["cash"] = math.floor(float(row["cash"]) * 100) / 100
        data[0]["totalSales"] = math.floor(float(stockVal) * 100) / 100
        data[0]["totalGrand"] = math.floor(float(cash + stockVal) * 100) / 100
        print(data)
    return render_template("index.html", data=data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "POST":
        shares = request.form.get("shares")
        # print("*****shares: " + str(shares) + " is a digit?: " + str(str(shares).isdigit()))
        if not str(shares).isnumeric():
            return apology("Only whole numbers allowed. Enter 1 or more shares", 400)
        if "." in str(shares):
            return apology(
                "partial shares are not supported, enter a whole number", 400
            )
        shares = int(shares)
        if shares < 1 or str(shares).isnumeric() == False:
            return apology("must enter 1 or more shares", 400)
        print(request.form.get("symbol"))
        if lookup(request.form.get("symbol")) is None:
            return apology("symbol not found", 400)
        if request.form.get("symbol") is None or len(request.form.get("symbol")) == 0:
            return apology("search for a symbol", 400)
        # if str(request.form.get("shares")).isdecimal():
        #     return apology("partial shares are not supported, enter a whole number", 400)

        price = lookup(request.form.get("symbol"))
        symbol = price["symbol"]
        price = math.floor(float(price["price"]) * 100) / 100
        # price[0]['price'] = math.floor(float(price[0]['price']) * 100) / 100
        cost = shares * price
        userDB = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if cost > float(userDB[0]["cash"]):
            return apology("insufficient funds", 400)

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?", cost, session["user_id"]
        )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, purchase_price, quantity) VALUES(?, ?, ?, ?)",
            session["user_id"],
            symbol,
            cost,
            shares,
        )
        walletDB = db.execute(
            "SELECT symbol FROM wallet WHERE user_id = ? AND symbol = ?",
            session["user_id"],
            symbol,
        )
        if len(walletDB) == 0:
            db.execute(
                "INSERT INTO wallet (user_id, symbol, quantity) VALUES(?, ?, ?)",
                session["user_id"],
                symbol,
                shares,
            )
        else:
            db.execute(
                "UPDATE wallet SET quantity = quantity + ? WHERE user_id = ? AND symbol = ?",
                shares,
                session["user_id"],
                symbol,
            )
        # print("******** Purchase Success. Shares: " + str(shares) + " symbol: " + str(symbol) +
        #         " price per share: " + str(price) + " total price: " + str(cost))
        # return render_template("purchased.html", price=price, total=cost, shares=shares, symbol=symbol)
        return redirect("/")
    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    data = db.execute(
        "SELECT symbol, purchase_price, sale_price, quantity, timestamp FROM transactions WHERE user_id = ? ORDER BY timestamp ASC",
        session["user_id"],
    )
    for row in data:
        if row["purchase_price"] is None:
            row["sale_price_value_per_share"] = usd(
                math.floor(float(row["sale_price"]) / float(row["quantity"]) * 100)
                / 100
            )
            row["sale_price"] = usd(float(row["sale_price"]))
            row["purchase_price"] = ""
            row["quantity"] = str(row["quantity"]) + " sell"
        else:
            row["purchase_price_value_per_share"] = usd(
                math.floor(float(row["purchase_price"]) / float(row["quantity"]) * 100)
                / 100
            )
            row["purchase_price"] = usd(float(row["purchase_price"]))
            row["sale_price"] = ""
            row["quantity"] = str(row["quantity"]) + " buy"
    print(data)
    return render_template("history.html", data=data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        print("******* in quote post")
        print(request.form.get("symbol"))
        if request.form.get("symbol") is None:
            print("error in lookup()")
            return apology("symbol not found", 400)

        symbol = request.form.get("symbol")
        data = lookup(symbol)

        if data is None:
            print("symbol not found")
            return apology("symbol not found", 400)

        data = [data]
        print(data)
        price = math.floor(data[0]["price"] * 100) / 100
        symbol = data[0]["symbol"]
        print(price)
        print(symbol)
        print(data)
        # if request.form.get("type") == "quote":
        return render_template("quoted.html", price=price, symbol=symbol)
        # if request.form.get("type") == "buy":
        #     return render_template("buy.html", price=price, symbol=symbol)
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 400)
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords must match", 400)

        try:
            db.execute(
                "INSERT INTO users(username, hash) VALUES(?, ?)",
                request.form.get("username"),
                generate_password_hash(request.form.get("password")),
            )
            return redirect("/")
        except:
            return apology("user exists, please sign in", 400)
    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        shares = float(request.form.get("shares"))
        print("***** shares: " + str(shares))
        price = lookup(request.form.get("symbol"))
        if len(price) == 0:
            return apology(
                "must enter a ticker symbol and number of shares to sell", 400
            )
        print("**** shares numeric? " + str(str(shares).isnumeric()))
        # if not str(shares).isnumeric():
        #     return apology("must enter a whole number to sell shares", 400)
        # if '.' in str(shares):
        #     return apology("partial shares are not supported, enter a whole number", 400)
        shares = int(shares)
        if shares < 1 or str(shares).isnumeric() == False:
            return apology("must enter 1 or more shares", 400)

        cost = float(shares) * float(price["price"])
        walletdb = db.execute(
            "SELECT * FROM wallet WHERE user_id = ? and symbol = ?",
            session["user_id"],
            price["symbol"],
        )
        quantityOwned = walletdb[0]["quantity"]
        if shares > quantityOwned:
            return apology(
                "cannot enter a number of shares greater than the amount owned", 400
            )

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?", cost, session["user_id"]
        )
        db.execute(
            "INSERT INTO transactions (user_id, symbol, sale_price, quantity) VALUES(?, ?, ?, ?)",
            session["user_id"],
            price["symbol"],
            cost,
            shares,
        )
        db.execute(
            "UPDATE wallet SET quantity = quantity - ? WHERE user_id = ? AND symbol = ?",
            shares,
            session["user_id"],
            price["symbol"],
        )
        print("******** Sale Success")
        return redirect("/")
    if request.method == "GET":
        data = db.execute(
            "SELECT DISTINCT wallet.symbol, wallet.quantity, users.cash FROM users JOIN wallet ON users.id = wallet.user_id JOIN transactions ON wallet.user_id = transactions.user_id WHERE users.id = ? AND wallet.quantity IS NOT '0' ORDER BY wallet.symbol ASC",
            session["user_id"],
        )
        print(data)
        for row in data:
            price = lookup(row["symbol"])
            row["current_price_per_share"] = price["price"]
            row["current_value"] = price["price"] * row["quantity"]
            row["cash"] = float(row["cash"])
        return render_template("sell.html", data=data)

    return render_template("sell.html")
