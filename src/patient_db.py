"""patient_db module"""

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import operators
from sqlalchemy import select
from patient_db_config import PATIENTS_TABLE, ENGINE


class PatientDB:

    def __init__(self):
        pass

    def insert_patient(self, request_body):

        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.insert().values(**request_body)
            result = conn.execute(stmt)
            conn.commit()
            return request_body['patient_id']
        except SQLAlchemyError as e:
            print("Error occurred while inserting the patient", e)
            return None
        finally:
            conn.close()

    def row_to_dict(self, row_keys, row_values):

        return dict(zip(row_keys, row_values))

    def select_all_patients(self):

        try:
            conn = ENGINE.connect()
            stmt = select(PATIENTS_TABLE)
            result = conn.execute(stmt)
            keys = result.keys()
            rows = result.fetchall()
            patients = [dict(zip(keys, row)) for row in rows]
            return patients
        except SQLAlchemyError as e:
            print("Error occurred while selecting all patients", e)
            return None
        finally:
            conn.close()

    def fetch_patient_id_by_name(self, patient_name):

        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select().where(
                operators.like_op(
                    PATIENTS_TABLE.c.patient_name,
                    "%"+patient_name+"%"
                )
            )
            result = conn.execute(stmt)
            keys = result.keys()
            rows = result.fetchall()
            patients = [dict(zip(keys, row)) for row in rows]
            return patients
        except SQLAlchemyError as e:
            print("Error occurred while fetching patient ID by name", e)
            return None
        finally:
            conn.close()

    def select_patient(self, patient_id):

        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.select().where(
                PATIENTS_TABLE.c.patient_id == patient_id
            )
            result = conn.execute(stmt)
            keys = result.keys()
            values = result.fetchone()
            patient = self.row_to_dict(keys, values)
            return patient
        except SQLAlchemyError as e:
            print("Error occurred while selecting the patient", e)
            return None
        finally:
            conn.close()

    def update_patient(self, patient_id, update_dict):

        try:
            conn = ENGINE.connect()
            stmt = (
                PATIENTS_TABLE.update()
                .where(PATIENTS_TABLE.c.patient_id == patient_id)
                .values(**update_dict)
            )
            result = conn.execute(stmt)
            conn.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while updating the patient", e)
            return None
        finally:
            conn.close()

    def delete_patient(self, patient_id):

        try:
            conn = ENGINE.connect()
            stmt = PATIENTS_TABLE.delete().where(
                PATIENTS_TABLE.c.patient_id == patient_id
            )
            result = conn.execute(stmt)

            conn.commit()
            return result.rowcount
        except SQLAlchemyError as e:
            print("Error occurred while deleting the patient", e)
            return None
        finally:
            conn.close()