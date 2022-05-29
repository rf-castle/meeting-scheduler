from calendar import calendar
from flask import Flask, request, jsonify
from calendar_test import Calendar
from calendarController import calendarController

app = Flask(__name__)

@app.route("/")
def index():
    test = "testaaaa"
    return calendarController.testController(test)

@app.route("/test")
def test():
    return jsonify(calendarController.testController())

# 空いている日程を取得
@app.route("/empty-dates")
def getEmptyDates():
    return jsonify(calendarController.getEmptyDates())

# 候補日を登録
@app.route("/candidate-dates", methods=['POST'])
def registerCandidates():
    company_name = str(request.form.get("company"))
    candidate_dates = request.form.get("candidate_dates")
    return jsonify(calendarController.registerCandidates(company_name, candidate_dates)), 201

# 面接日を登録
@app.route("/interview-date", methods=['POST'])
def registerInterviewDate():
    company_name = str(request.form.get("company"))
    interview_dates = request.form.get("candidate_dates")
    print(interview_dates)
    return jsonify(calendarController.registerInterviewDate(company_name, interview_dates)), 201

# 面接一覧取得（本日からのやつ）
@app.route("/interview-dates", methods=['GET'])
def fetchInterviewDates():
    return jsonify(calendarController.fetchInterviewDates()), 200

# ある企業の候補日一覧取得
@app.route("/interview-dates/<company_name>", methods=["GET"])
def fetchInterviewDatesByCompanyName(company_name):
    # try 必要？
    return jsonify(calendarController.fetchCandidateDatesByCompanyName(company_name)), 200



@app.route("/calendar-permission")
def getUrlForPermission():
    url = calendarController.getUrlForPermission()
    return url

@app.route("/oauth2callback")
def storeCredentials():
    print(request.args.get("code"))
    calendarController.storeCredentials(request.args.get("code"))
    return "カレンダーの連携完了"



@app.route("/calendar-list")
def fetchEventList():

    # print(calendarController.registerCandidates("F 株式会社", ["6/5 10:00 - 12:00", "6/7 10:00 - 12:00"]))
    print(calendarController.registerInterviewDate("F 株式会社", "6/5 10:00 - 11:00"))
    # print(calendarController.fetchInterviewDates())
    # print(calendarController.fetchCandidateDatesByCompanyName("F 株式会社"))
    # print(calendarController.getEmptyDates())
    return "取得"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
