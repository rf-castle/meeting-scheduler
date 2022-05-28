from flask import Flask, request, jsonify
from calendar_test import Calendar
from calendarController import calendarController

app = Flask(__name__)

@app.route("/")
def index():
    test = "testaaaa"
    return calendarController.testController(test)

# 空いている日程を取得
@app.route("/empty-dates")
def getEmptyDates():
    return jsonify(calendarController.getEmptyDates())

# 候補日を登録
@app.route("/candidate-dates", methods=['POST'])
def registerCandidates():
    company_name = str(request.form.get("company"))
    candidate_dates = request.form.get("candidate_dates")
    return jsonify(calendarController.registerCandidates(company_name, candidate_dates))

# 面接日を登録
@app.route("/interview-date", methods=['POST'])
def registerInterviewDate():
    company_name = str(request.form.get("company"))
    interview_dates = request.form.get("candidate_dates")
    return jsonify(calendarController.registerInterviewDate(company_name, interview_dates))


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
