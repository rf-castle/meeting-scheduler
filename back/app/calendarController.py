class calendarController():
    def getHtml(self):
        return "<h1>test Class</h1>"

    @staticmethod
    def testController(testText):
        return "test controller " + testText

    @staticmethod
    def getEmptyDates():
        # calendar API
        empty_dates = ("2022-05-26", "2022-05-27")
        return empty_dates

    @staticmethod
    def registerCandidates(company_name, candidate_dates):
        # 候補日を登録

        #（日程確認メール送信）
        
        status_code = 200
        return status_code

    @staticmethod
    def registerInterviewDate(company_name, interview_dates):
        #面接日を登録

        #（候補日を削除）
        
        status_code = 200
        return status_code
