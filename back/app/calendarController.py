from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
import datetime
import lib.util as util

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = "http://localhost:9000/oauth2callback"


class calendarController():

    @staticmethod
    def testController():
        return util.getWholeEmptyTimes()

    @staticmethod
    def getEmptyDates():
        # calendar API
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        busy_times = (
            {
                "start": "2022-05-28T15:00:00+09:00",
                "end": "2022-05-28T16:00:00+09:00"
            },
            {
                "start": "2022-05-29T11:00:00+09:00",
                "end": "2022-05-29T12:00:00+09:00"
            },
            {
                "start": "2022-05-29T13:00:00+09:00",
                "end": "2022-05-29T17:00:00+09:00"
            }
        )
        empty_dates = util.calcEmptyDate(busy_times)

        #empty_dates = ("2022-05-26", "2022-05-27")
        return empty_dates

    @staticmethod
    def registerCandidates(company_name, candidate_dates):
        # calendar API
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        # 候補日を登録

        #（日程確認メール送信）
        
        status_code = 200
        return status_code

    @staticmethod
    def registerInterviewDate(company_name, interview_dates):
        # calendar API
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        #面接日を登録

        #（候補日を削除）
        
        status_code = 200
        return status_code

    @staticmethod
    def getUrlForPermission():

        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        flow.redirect_uri=REDIRECT_URI
        url_for_permission, _ = flow.authorization_url()
        return url_for_permission

    @staticmethod
    def storeCredentials(code):
        
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        flow.redirect_uri=REDIRECT_URI
        flow.fetch_token(code=code)
        creds = flow.credentials
        with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return 
    
    @staticmethod
    def fetchEventList():

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)


        # 予定の取得
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=10, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            # dateTime: 時間指定の予定だったら，ここに入る
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(type(start))
            print(start, event['summary'])

        return 
