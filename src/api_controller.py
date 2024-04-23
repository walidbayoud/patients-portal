"""Patient API Controller"""

from flask import Flask , request , jsonify
from patient_db import PatientDB

class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):

        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)



    def create_patient(self):
        try:
            request_body = request.json
            patient_id = self.patient_db.insert_patient(request_body)
            if patient_id:
                return jsonify({"patient_id": patient_id}), 200
            else:
                return jsonify({"error": "Failed to create patient"}), 400
        except Exception as e:
            import traceback
            traceback.print_exc()  # Print the traceback
            return jsonify({"error": str(e)}), 400

    def get_patients(self):
        patients = self.patient_db.select_all_patients()
        if patients:
            return jsonify(patients), 200
        else:
            return jsonify({"error": "Failed to retrieve patients"}), 400

    def get_patient(self, patient_name):
        print(patient_name)
        patient = self.patient_db.fetch_patient_id_by_name(patient_name)
        if patient:
            return jsonify(patient), 200
        else:
            return jsonify({"error": "Patient not found"}), 404

    def update_patient(self, patient_id):
        try:
            update_data = request.json
            num_updated = self.patient_db.update_patient(patient_id, update_data)
            if num_updated is not None:
                return jsonify({"message": f"Updated {num_updated} patient(s)"}), 200
            else:
                return jsonify({"error": "Failed to update patient"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def delete_patient(self, patient_id):
        num_deleted = self.patient_db.delete_patient(patient_id)
        if num_deleted is not None:
            return jsonify({"message": f"Deleted {num_deleted} patient(s)"}), 200
        else:
            return jsonify({"error": "Failed to delete patient"}), 400

    def run(self):
        self.app.run()


PatientAPIController()