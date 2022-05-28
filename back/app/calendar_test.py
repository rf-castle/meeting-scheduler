from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/calendar']
PORT = 9000
REDIRECT_URI = "http://localhost:9000/oauth2callback"

class Calendar:

    def get_url_for_permission():

        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
        flow.redirect_uri=REDIRECT_URI
        url_for_permission, _ = flow.authorization_url()
        print(url_for_permission)
        return url_for_permission


    def store_credentials(code):
        print("store!!")
        flow = InstalledAppFlow.from_client_secrets_file(
                'credentials2.json', SCOPES)
        flow.redirect_uri=REDIRECT_URI
        flow.fetch_token(code=code)
        creds = flow.credentials
        with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return 
       
    def fetch_event_list():

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

        

    