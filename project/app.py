# Moved this import below the db variable so that the functions in helpers.py have access to it.
# Pushed the rest to the top to properly call out that they are from CS50
# TODO: Remove apology, rewrite login / logout pages.
from helpers import (
    apology,
    login_required,
    lookup,
    usd,
    checkQueue,
    clearKeyEntry,
    logRequest,
)

# Lib I imported for json.dumps() function to convert a dict to JSON
import json

# START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT
import os
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Custom filter
app.jinja_env.filters["usd"] = usd
# END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT

request_log = {}

# START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
    # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


@app.route("/", methods=["GET"])
@login_required
def index():
    """Show portfolio of stocks"""

    return render_template("/index.html")


@app.route("/wallet", methods=["GET"])
@login_required
def wallet():
    if session["user_id"] == None:
        return redirect("/login")
    if request.method == "GET":
        data = db.execute(
            """SELECT DISTINCT wallet.symbol, wallet.quantity, users.cash
                          FROM users JOIN wallet ON users.id = wallet.user_id
                          JOIN transactions ON wallet.user_id = transactions.user_id
                          WHERE users.id = ? ORDER BY wallet.symbol ASC""",
            session["user_id"],
        )
        if len(data) == 0:
            return jsonify({"error": "No transaction records found"}), 400
        transactions = db.execute(
            """SELECT * FROM transactions WHERE user_id = ? ORDER BY "symbol" ASC""",
            session["user_id"],
        )
        if len(transactions) == 0:
            return jsonify({"error": "No transaction records found"}), 400
        for row in data:
            price = lookup(row["symbol"])
            if price is None:
                return jsonify({"error": "No response from Yahoo's server"})
            row["current_price_per_share"] = usd(price["price"])
            row["current_value"] = usd(price["price"] * row["quantity"])
            row["cash"] = usd(float(row["cash"]))
            row["longName"] = price["longName"]
            row["shortName"] = price["shortName"]
            row["exchange_timezone"] = price["exchange_timezone"]
            row["previous_close"] = usd(price["previous_close"])
            row["current_price_vs_previous_close"] = (
                price["price"] - price["previous_close"]
            )
            row["wallet_value"] = 0
            for transaction in transactions:
                if transaction["symbol"] == row["symbol"]:
                    if transaction["purchase_price"] is None:
                        row["wallet_value"] -= int(transaction["sale_price"] * 100)
                    else:
                        row["wallet_value"] += int(transaction["purchase_price"] * 100)
            row["wallet_value"] = row["wallet_value"] / 100
            row["current_val_vs_wallet_val"] = (price["price"] * row["quantity"]) - row[
                "wallet_value"
            ]
        return jsonify(data)
    return render_template("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        data = request.get_json()
        if len(data) == 0:
            print("***** Data empty")
            return jsonify({"error": "no data sent in POST request"}), 400
        # print("******* printing data")
        # print(data)
        end_point = "/buy"
        method = request.method
        hashkey = data["hashkey"]
        # print(method)
        print(data["symbol"])
        user_request = {"symbol": data["symbol"], "shares": data["shares"]}
        user_request = json.dumps(user_request)
        shares = float(data["shares"])
        if shares < 0.0001 or shares is None:
            return (
                jsonify({"error": "Shares value must be a number greater than 0.0001"}),
                400,
            )
        # print(user_request)
        # print(session["user_id"])
        # print(key)
        if (
            checkQueue(
                request_log,
                session["user_id"],
                hashkey,
                method,
                end_point,
                user_request,
            )
            is None
        ):
            return jsonify({"error": "Server is handing your previous request"})
        try:
            try:
                print("***** looking up the symbol")
                symbol = lookup(data["symbol"])
                print("***** symbol retrieved: " + str(symbol))
            except:
                print("**** no symbol")
                logRequest(request_log, hashkey, 400)
                return (
                    jsonify({"error": "could not find stock symbol, please try again"}),
                    400,
                )
            cost = shares * symbol["price"]
            # print(session["user_id"])
            funds = db.execute("SELECT cash FROM users WHERE id=?", session["user_id"])
            # print("funds: " + str(funds[0]["cash"]))
            if cost < float(funds[0]["cash"]):
                # print("cost: " + str(cost))
                db.execute(
                    """UPDATE users SET cash = cash - ? WHERE id = ?""",
                    cost,
                    session["user_id"],
                )
                db.execute(
                    """INSERT INTO transactions (user_id, symbol, purchase_price, quantity,
                        cash_balance) VALUES(?, ?, ?, ?, ?)""",
                    session["user_id"],
                    symbol["symbol"],
                    cost,
                    shares,
                    float(funds[0]["cash"]) - cost,
                )
                checkDB = db.execute(
                    """SELECT symbol FROM wallet WHERE user_id = ? AND symbol = ?""",
                    session["user_id"],
                    symbol["symbol"],
                )
                if len(checkDB) == 0:
                    db.execute(
                        """INSERT INTO wallet (user_id, symbol, quantity) VALUES(?, ?, ?)""",
                        session["user_id"],
                        symbol["symbol"],
                        shares,
                    )
                else:
                    db.execute(
                        """UPDATE wallet SET quantity = quantity + ? WHERE user_id = ? AND symbol = ?""",
                        shares,
                        session["user_id"],
                        symbol["symbol"],
                    )
                    print("********** after DB update")
                print("******** Purchase Success")
                logRequest(request_log, hashkey, 200)
                return jsonify({"message": "Purchase successful."}), 200
            else:
                print("**** insufficient funds")
                logRequest(request_log, hashkey, 412)
                return jsonify({"error": "Purchase cancelled. Insufficent funds"}), 412
        except:
            try:
                print("**** failed out of buy")
                logRequest(request_log, hashkey, 500)
                return (
                    jsonify({"error": "SERVER ERROR: Purchase could not be processed"}),
                    500,
                )
            except:
                print("**** failed out of buy, couldn't write to db")
                clearKeyEntry(request_log, hashkey)
                return (
                    jsonify(
                        {"error": "SERVER ERROR: Failed to log failure to purchase"}
                    ),
                    500,
                )
        # check if the user has enough money to buy the stock
        # add the stock purchase to their account and remove the price from their account

    return render_template("buy.html")


@app.route("/showHistory")
@login_required
def showHistory():
    data = db.execute(
        """SELECT symbol, purchase_price, sale_price, quantity,
                      timestamp, cash_balance FROM transactions
                      WHERE user_id = ? ORDER BY timestamp DESC LIMIT 50""",
        session["user_id"],
    )
    if len(data) == 0:
        return jsonify({"error": "No transaction history"}), 400
    symbols = {}
    for row in data:
        if row["symbol"] not in symbols:
            symbols[row["symbol"]] = row["symbol"]
            symbols[row["symbol"]] = lookup(row["symbol"])
            print("***** added symbol")
            print(symbols)

        row["longName"] = symbols[row["symbol"]]["longName"]
        row["shortName"] = symbols[row["symbol"]]["shortName"]
        row["previous_close"] = usd(symbols[row["symbol"]]["previous_close"])
        if row["sale_price"] is None:
            row["purchase_price"] = usd(row["purchase_price"])
        else:
            row["sale_price"] = usd(row["sale_price"])
        row["cash_balance"] = usd(row["cash_balance"])
        row["previous_close"] = usd(symbols[row["symbol"]]["previous_close"])
    return jsonify(data)


@app.route("/history")
@login_required
def history():
    return render_template("history.html")

    # START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            # hashBool = check_password_hash(row[0]["hash"], request.form.get("password"))
            # return apology(f"invalid username and/or password. HashBool = {hashBool}", 400)
            return apology("invalid username and/or password.", 400)
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
    # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        symbol = request.get_json()
        symbol = symbol["symbol"]
        stock = lookup(symbol)

        if symbol is None:
            return jsonify({"error": "Type in a stock into the input field"}), 400
        if stock is None:
            print("******* stock not found or Yahoo is not responding")
            return jsonify({"error": "Stock not found"}), 400

        stock["current_price_vs_previous_close"] = (
            int(stock["price"] * 100) - int(stock["previous_close"] * 100)
        ) / 100
        stock["price"] = usd(stock["price"])
        stock["previous_close"] = usd(stock["previous_close"])
        return jsonify(stock)

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
                """INSERT INTO users(username, hash) VALUES(?, ?)""",
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
    """Sell shares of stock"""
    if request.method == "POST":
        # print("*** POST CALLED")
        data = request.get_json()
        if len(data) == 0:
            print("***** Data empty")
            return jsonify({"error": "no data sent in POST request"}), 400
        end_point = "/sell"
        method = request.method
        hashkey = data["hashkey"]
        user_request = {"symbol": data["symbol"], "shares": data["shares"]}
        user_request = json.dumps(user_request)
        symbol = data.get("symbol")
        shares = float(data["shares"])
        if shares < 0.0001 or shares is None:
            return (
                jsonify(
                    {
                        "error": "Enter the number of shares you wish to sell. Must be over 0.0001"
                    }
                ),
                400,
            )

        if (
            checkQueue(
                request_log,
                session["user_id"],
                hashkey,
                method,
                end_point,
                user_request,
            )
            is None
        ):
            return jsonify({"error": "Server is handing your previous request"})
        try:
            # print("***** shares: " + str(shares) + " symbol: " + symbol)
            walletdb = db.execute(
                """SELECT * FROM wallet WHERE user_id = ? and symbol = ?""",
                session["user_id"],
                symbol,
            )
            owned = walletdb[0]["quantity"]
            print("********owned: " + str(owned) + "shares: " + str(shares))
            if owned is None or owned < shares:
                logRequest(request_log, hashkey, 412)
                return (
                    jsonify(
                        {"error": "insufficient owned shares to make the transaction"}
                    ),
                    412,
                )
            else:
                # get price of shares from lookup()
                amount = lookup(symbol)
                value = shares * amount["price"]
                cash = db.execute(
                    "SELECT cash FROM users WHERE id = ?", session["user_id"]
                )
                print(
                    "Sale value: "
                    + str(value)
                    + " shares: "
                    + str(shares)
                    + " amount per share: "
                    + str(amount["price"])
                )
                # put the transaction record in sales
                db.execute(
                    """INSERT INTO transactions (user_id, symbol, sale_price, quantity, cash_balance)
                        VALUES(?, ?, ?, ?, ?)""",
                    session["user_id"],
                    symbol,
                    value,
                    shares,
                    float(cash[0]["cash"]) + value,
                )
                # update the user's cash in users
                db.execute(
                    """UPDATE users SET cash = cash + ? WHERE id = ?""",
                    value,
                    session["user_id"],
                )
                # update the user's wallet to remove the share(s)
                db.execute(
                    """UPDATE wallet SET quantity = quantity - ? WHERE user_id = ? AND symbol = ?""",
                    shares,
                    session["user_id"],
                    symbol,
                )
                # do sale and track changes in wallet and the sales databases
                logRequest(request_log, hashkey, 200)
                return (
                    jsonify(
                        {
                            "message": "sale successful. Stock: "
                            + symbol
                            + " Shares: "
                            + str(shares)
                            + " Total: "
                            + usd(value)
                        }
                    ),
                    200,
                )
        except:
            try:
                print("**** failed out of sell")
                logRequest(request_log, hashkey, 500)
                return (
                    jsonify({"error": "SERVER ERROR: Sell could not be processed"}),
                    500,
                )
            except:
                print("**** failed out of sell, couldn't write to db")
                clearKeyEntry(request_log, hashkey)
                return (
                    jsonify({"error": "SERVER ERROR: Failed to log failure to sell"}),
                    500,
                )
    return render_template("sell.html")


@app.route("/sell_details", methods=["GET"])
@login_required
def sell_details():
    if request.method == "GET":
        # print("*********** in sell get")
        data = db.execute(
            """SELECT symbol, quantity FROM wallet
                          WHERE user_id = ? ORDER BY symbol ASC;""",
            session["user_id"],
        )
        if len(data) == 0:
            return jsonify({"error": "No stocks found in wallet"})
        for row in data:
            price = lookup(row["symbol"])
            if price is None:
                return jsonify(
                    {
                        "error": f"Failed to look up price for {row['symbol']}. Please try again."
                    }
                )
            row["current_price_per_share"] = usd(price["price"])
        # print("****** Sending response")
        return jsonify(data)
    return render_template("sell.html")
