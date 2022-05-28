from flask import Flask, request
from calendar_test import Calendar

app = Flask(__name__)


@app.route("/")
def index():
    return "<h1>Hello, Flask!</h1>"


@app.route("/calendar-permission")
def get_url_for_permission():
    url = Calendar.get_url_for_permission()
    return url

@app.route("/oauth2callback")
def store_credentials():
    print(request.args.get("code"))
    Calendar.store_credentials(request.args.get("code"))
    return "カレンダーの連携完了"


@app.route("/calendar-list")
def fetch_event_list():
    Calendar.fetch_event_list()
    return "取得"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
