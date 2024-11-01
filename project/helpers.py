import csv
import datetime
import pytz
import requests
import urllib
import uuid
import json
from flask import redirect, render_template, request, session
from functools import wraps
from app import db

# START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function
    # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


def lookup(symbol):
    """Look up quote for symbol."""
    # Test data here if Yahoo API cannot be accessed:
    # if symbol == 'AAAA': return {"price": 28, "symbol": 'AAAA'}
    # if symbol == 'BBBB': return {"price": 2.5, "symbol": 'BBBB'}

    # Prepare API request
    symbol = symbol.upper()
    end = datetime.datetime.now(pytz.timezone("US/Eastern"))
    start = end - datetime.timedelta(days=7)

    # Yahoo Finance API
    # updated endpoint from reddit: https://www.reddit.com/r/sheets/comments/1farvxr/comment/llxk7m9/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # The url FUNCTIONALITY FROM CS50 FINANCE PROJECT
    url = (
        f"https://query2.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote_plus(symbol)}"
        f"?period1={int(start.timestamp())}"
        f"&period2={int(end.timestamp())}"
        f"&interval=1d&events=history"
    )

    # Query API
    # START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT
    try:
        response = requests.get(
            url,
            cookies={"session": str(uuid.uuid4())},
            headers={"Accept": "*/*", "User-Agent": request.headers.get("User-Agent")},
        )
        response.raise_for_status()
        # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT
        # converting the response from bit format to utf-8, and then into JSON. Filtering down to the desired content.
        data = json.loads(str(response.content, "utf-8"))["chart"]["result"][0]["meta"]
        # print(data)
        price = float(int(data["regularMarketPrice"] * 100) / 100)
        symbol = data["symbol"]
        longName = data["longName"]
        shortName = data["shortName"]
        exchangeTimezoneName = data["exchangeTimezoneName"]
        chartPreviousClose = data["chartPreviousClose"]
        return {
            "price": price,
            "symbol": symbol,
            "longName": longName,
            "shortName": shortName,
            "exchange_timezone": exchangeTimezoneName,
            "previous_close": chartPreviousClose,
        }
    # START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT
    except (KeyError, IndexError, requests.RequestException, ValueError):
        return None
    # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT

    # START OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"
    # END OF FUNCTIONALITY FROM CS50 FINANCE PROJECT


def checkQueue(request_log, user_id, hashkey, method, end_point, user_request):
    try:
        if request_log[hashkey] is not None:
            print("**** found duplicate user in checkQueue")
            return None

    except:
        request_data = {
            "user_id": user_id,
            "method": method,
            "end_point": end_point,
            "request": user_request,
        }
        request_log[hashkey] = request_data

        print("**** user added")
        print(request_log)
        return 1


def logRequest(request_log, hashkey, status_code):
    print("***** In log request")
    try:
        db.execute(
            """INSERT INTO audit (key, user_id, end_point, method, request, status_code) VALUES(?, ?, ?, ?, ?, ?)""",
            hashkey,
            request_log[hashkey]["user_id"],
            request_log[hashkey]["end_point"],
            request_log[hashkey]["method"],
            request_log[hashkey]["request"],
            status_code,
        )
        print("***** db.execute done")
    except Exception as e:
        print(f"***** db.execute failed: {e}")
    print("**** clearing key via logRequest")
    clearKeyEntry(request_log, hashkey)
    return None


def clearKeyEntry(request_log, hashkey):
    print("***** in clearKeyEntry")
    print(request_log)
    print("**** deleting key: " + hashkey)
    try:
        del request_log[hashkey]
        print(request_log)
        print("**** deleted Key")
        return 1
    except:
        print("**** failed to delete key: " + hashkey)
        return None
