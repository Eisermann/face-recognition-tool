import datetime
import logging
import os.path
import pickle
import typing

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

LOGGER = logging.getLogger()

TOKEN_FILE_NAME = "token.pickle"


class GoogleCalendarApi:

    def __init__(
        self,
        scopes: typing.List[str],
        credentials_file: str,
    ):
        self.scopes = scopes
        self.credentials_file = credentials_file

        credentials = None

        if os.path.exists(TOKEN_FILE_NAME):
            credentials = self._load_credentials()

        if not (credentials and credentials.valid):
            credentials = self._log_in(credentials)

        self.service = build("calendar", "v3", credentials=credentials)

    def load_events(
        self,
        time_min: str = None,
        time_max: str = None,
        max_results: int = 10
    ) -> typing.List[dict]:
        if not time_min:
            time_min = self.get_now()

        events_result = self.service.events().list(
            calendarId="primary",  # todo: should be taken from user
            timeMin=time_min,
            timeMax=time_max,
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])

        if not events:
            LOGGER.info("No upcoming events found.")

        return events

    @staticmethod
    def get_now():
        return datetime.datetime.utcnow().isoformat() + "Z"

    @staticmethod
    def get_end_of_day():
        now = datetime.datetime.utcnow()
        return datetime.datetime(
            year=now.year, month=now.month, day=now.day, hour=23, minute=59, second=59
        ).isoformat() + "Z"

    @staticmethod
    def _load_credentials():
        with open(TOKEN_FILE_NAME, "rb") as token:
            return pickle.load(token)

    def _log_in(self, credentials):
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials_file, self.scopes
            )
            credentials = flow.run_local_server()

        with open(TOKEN_FILE_NAME, "wb") as token:
            pickle.dump(credentials, token)

        return credentials
