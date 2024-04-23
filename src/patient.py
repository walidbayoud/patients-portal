import requests
from uuid import uuid4
from datetime import datetime
import config

class Patient:
    def __init__(self, name, gender, age):
        self.id = str(uuid4())
        self.name = name
        self.gender = gender
        self.age = age
        self.checkin = datetime.now().strftime(config['date_time_format'])
        self.checkout = None
        self.ward = None
        self.room = None

    def update_room_and_ward(self, ward, room):
        self.ward = ward
        self.room = room

    def commit_to_database(self, api_url):
        patient_data = {
            'patient_id': self.id,
            'patient_name': self.name,
            'patient_age': self.age,
            'patient_gender': self.gender,
            'patient_checkin': self.checkin,
            'patient_checkout': self.checkout,
            'patient_ward': self.ward,
            'patient_room': self.room
        }

        try:
            if self.id:
                response = requests.put(f"{api_url}/patients/{self.id}", json=patient_data)
            else:
                response = requests.post(f"{api_url}/patients", json=patient_data)

            if response.status_code == 200:
                print("Patient successfully committed to the database.")
            else:
                print("Failed to commit patient to the database:", response.json())
        except Exception as e:
            print("An error occurred:", e)
