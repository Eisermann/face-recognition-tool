import json
import typing


class EmployeeData:
    id: int
    status: str
    office_room: str
    name: str
    email: str

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)


class DatabaseApi:
    db: typing.Dict[int, EmployeeData]

    def __init__(self, file_name: str):
        with open(file_name) as json_db:
            json_data = json.load(json_db)
            self.db = {
                user_data["id"]: EmployeeData(**user_data)
                for user_data in json_data["users"]
            }

    def get_employee_data(self, requested_id: int) -> EmployeeData:
        return self.db[requested_id]
