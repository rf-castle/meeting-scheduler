from flask import Flask, jsonify, request
app = Flask(__name__)

from calendarController import calendarController

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
