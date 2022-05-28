from google.oauth2.credentials import Credentials
# from back.app.calendar_test import Calendar
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from parse import *
from calendar_api import CalendarAPI
import lib.util as util

#### 必ず Google Calendar の Timezone を日本にすること!!!!!!

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = "http://localhost:9000/oauth2callback"


class calendarController():

    @staticmethod
    def testController():
        return util.getWholeEmptyTimes()

    @staticmethod
    def getEmptyDates():

        busy_times = CalendarAPI.fetch_start_and_end_datetime_of_events()
        print(busy_times)
        
        empty_dates = util.calcEmptyDate(busy_times)

        #empty_dates = ("2022-05-26", "2022-05-27")
        return empty_dates

    @staticmethod
    def registerCandidates(company_name, candidate_dates):

        # calendar API
        response_dict = CalendarAPI.register_candidates(company_name, candidate_dates)

        #（日程確認メール送信）
        
        return response_dict

    @staticmethod
    def registerInterviewDate(company_name, interview_date):

        # calendar API
        response_dict = CalendarAPI.register_interview_date(company_name, interview_date)

        #（日程確認メール送信）
        return response_dict

    @staticmethod
    def fetchInterviewDates():

        response_dict = CalendarAPI.fetch_interview_dates()

        return response_dict

    @staticmethod
    def fetchCandidateDatesByCompanyName(company_name):

        response_dict = CalendarAPI.fetch_candidate_dates_by_company_name(company_name)

        return response_dict


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
    

    
