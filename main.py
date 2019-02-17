#!/usr/bin/python
import datetime
import logging

import coloredlogs
import face_recognition

from lib import Camera, DatabaseApi, GoogleCalendarApi, PhotosEncoder

LOGGER = logging.getLogger()

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
CREDENTIALS_FILE = "credentials.json"

coloredlogs.install(level=logging.INFO)
known_photos_loader = PhotosEncoder("known_photos")
users_api = DatabaseApi("users.json")
google_calendar_api = GoogleCalendarApi(scopes=SCOPES, credentials_file=CREDENTIALS_FILE)


def main():
    ids, encodings = known_photos_loader.load_photos()

    process_this_frame = True

    with Camera.open_camera():
        last_found_id = None

        while True:
            frame = Camera.get_frame()

            if process_this_frame:
                faces_locations = face_recognition.face_locations(frame)
                faces_encodings = face_recognition.face_encodings(frame, faces_locations)

                for face_encoding in faces_encodings:
                    matches = face_recognition.compare_faces(encodings, face_encoding)

                    if True in matches:
                        index = matches.index(True)
                        employee_id = ids[index]

                        if last_found_id != employee_id:
                            last_found_id = employee_id

                            show_employee_welcome(employee_id)
                    else:
                        if last_found_id is not None:
                            last_found_id = None
                            LOGGER.warning("Face not recognized.")

            process_this_frame = not process_this_frame


def show_employee_welcome(employee_id):
    employee_data = users_api.get_employee_data(employee_id)
    LOGGER.info(f"Recognized face of id {employee_id} - {employee_data.name}")

    say(f"Hello, {employee_data.name}!")

    events = google_calendar_api.load_events(time_max=google_calendar_api.get_end_of_day())

    if events:
        say(f"You have {len(events)} events today.")
    else:
        say("You have no more events today.")
        say(f"You can go to your room {employee_data.office_room}.")

    for event in events:
        start = event["start"].get("dateTime", None)

        if start:
            event = events[0]
            summary = event["summary"]
            location = event["location"]
            start_date_time = datetime.datetime.fromisoformat(start)

            say(f"{summary} will be in {location} and starts at "
                f"{start_date_time.hour}:{start_date_time.minute}")

            break


def say(text):
    print(text)


if __name__ == '__main__':
    main()
