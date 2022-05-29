from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from parse import *

SCOPES = ['https://www.googleapis.com/auth/calendar']
REDIRECT_URI = "http://localhost:9000/oauth2callback"
NUM_OF_FETCH_EVENT_FROM_GOOGLE_CALENDAR = 100

class CalendarAPI:

    @staticmethod
    def register_candidates(company_name, candidate_datetimes):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        for candidate_datetime in candidate_datetimes:

            # 候補日を登録
            start_datetime, end_datetime = CalendarAPI.format_by_rfc(candidate_datetime)
            event = {
                'summary': company_name + 'の候補日',
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': "Asia/Tokyo",
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': "Asia/Tokyo",
                },
            }
            event = service.events().insert(calendarId='primary',
                                        body=event).execute()


        company_name_and_candidate_dates = {}
        company_name_and_candidate_dates["company_name"] = company_name
        company_name_and_candidate_dates["candidate_dates"] = candidate_datetimes

        return company_name_and_candidate_dates

    @staticmethod
    def register_interview_date(company_name, interview_datetime):

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        # イベント全取得
        events = CalendarAPI.fetch_events(service)

        # 候補日を削除
        for event in events:
            if event['summary'] == company_name + 'の候補日':
                service.events().delete(calendarId='primary', eventId=event['id']).execute()

        # 面接日を登録
        start_datetime, end_datetime = CalendarAPI.format_by_rfc(interview_datetime)
        print(interview_datetime)
        print(start_datetime, end_datetime)
        event = {
                'summary': company_name + 'の面接日',
                'start': {
                    'dateTime': start_datetime,
                    'timeZone': "Asia/Tokyo",
                },
                'end': {
                    'dateTime': end_datetime,
                    'timeZone': "Asia/Tokyo",
                },
            }
        event = service.events().insert(calendarId='primary',
                                    body=event).execute()
        
        company_name_and_interview_date = {}
        company_name_and_interview_date["company_name"] = company_name
        company_name_and_interview_date["interview_date"] = interview_datetime

        return company_name_and_interview_date

    
    @staticmethod
    def fetch_interview_dates():

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        
        events = CalendarAPI.fetch_events(service)

        interview_dates_and_companies = []

        for event in events:
            if event['summary'].endswith('の面接日'):

                interview_date_and_company = {}

                result = parse("{company}の面接日", event['summary'])
                
                interview_date_and_company["company"] = result["company"]
                interview_date_and_company["interview_date"] = CalendarAPI.format_for_display(event['start']['dateTime'], event['end']['dateTime'])
                interview_dates_and_companies.append(interview_date_and_company)

        return interview_dates_and_companies

    
    @staticmethod
    def fetch_candidate_dates_by_company_name(company_name):

        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        service = build('calendar', 'v3', credentials=creds)

        events = CalendarAPI.fetch_events(service)

        interview_date_and_company = {}
        interview_date_and_company["company"] = company_name
        interview_date_and_company["candidate_dates"] = []

        for event in events:
            if event['summary'] == company_name + 'の候補日':
                interview_date_and_company["candidate_dates"].append(CalendarAPI.format_for_display(event['start']['dateTime'], event['end']['dateTime']))

        return interview_date_and_company


    @staticmethod
    def fetch_start_and_end_datetime_of_events():
        
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        calendar_service = build('calendar', 'v3', credentials=creds)

        events = CalendarAPI.fetch_events_in_two_weeks(calendar_service)
        start_and_end_datetime_by_rfc_of_events_list = []

        for event in events:
            start_and_end_datetime_by_rfc_of_event = {}
            if event['start'].get('dateTime') is None:
                continue
            start_and_end_datetime_by_rfc_of_event["start"] = event['start']['dateTime']
            start_and_end_datetime_by_rfc_of_event["end"] = event['end']['dateTime']
            start_and_end_datetime_by_rfc_of_events_list.append(start_and_end_datetime_by_rfc_of_event)

        return start_and_end_datetime_by_rfc_of_events_list



    @staticmethod
    def format_by_rfc(datetime_for_display):
        # datetime_for_display : 5/25 10:00 - 12:00
        # start_datetime_by_rfc: 2022-05-25T10:00
        # end_datetime_by_rfc: 2022-05-25T12:00

        result = parse("{month}/{day} {start_hour}:{start_minute} - {end_hour}:{end_minute}", datetime_for_display)
        start_datetime_by_rfc = "2022-" + result["month"] +"-" + result["day"] + "T" + result["start_hour"] + ":" + result["start_minute"] + ":00.000+09:00"
        end_datetime_by_rfc = "2022-" + result["month"] +"-" + result["day"] + "T" + result["end_hour"] + ":" + result["end_minute"] + ":00.000+09:00"
        
        return start_datetime_by_rfc, end_datetime_by_rfc

    @staticmethod
    def format_for_display(start_datetime_by_rfc, end_datetime_by_rfc):
        # tart_datetime_by_rfc, end_datetime_by_rfc: 2022-06-04T23:30:00+09:00, 2022-06-04T23:45:00+09:00
        # 06/04 23:30 - 23:45

        start_result = parse("{year}-{month}-{day}T{start_hour}:{start_minute}:{other}", start_datetime_by_rfc)
        end_result = parse("{other1}T{end_hour}:{end_minute}:{other2}", end_datetime_by_rfc)

        return start_result["month"] + "/" + start_result["day"] + " " + start_result["start_hour"] + ":" + start_result["start_minute"] + " - " + end_result["end_hour"] + ":" + end_result["end_minute"]

    @staticmethod
    def fetch_events(calendar_service):

        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
       
        events_result = calendar_service.events().list(calendarId='primary', timeMin=now,
                                            maxResults=NUM_OF_FETCH_EVENT_FROM_GOOGLE_CALENDAR, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events

    @staticmethod
    def fetch_events_in_two_weeks(calendar_service):

        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        after_two_weeks = (datetime.utcnow() +timedelta(weeks=2)).isoformat() + 'Z'
        print("2週間後")
        print(after_two_weeks)

        events_result = calendar_service.events().list(calendarId='primary', timeMin=now,
                                            timeMax=after_two_weeks,
                                            maxResults=NUM_OF_FETCH_EVENT_FROM_GOOGLE_CALENDAR, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        return events