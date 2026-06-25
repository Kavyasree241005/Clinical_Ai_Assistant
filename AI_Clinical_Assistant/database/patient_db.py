from database.mongodb import patients_collection


def create_patient(data):

    return patients_collection.insert_one(
        data
    )


def get_patient(
    patient_id
):

    return patients_collection.find_one(
        {
            "patient_id": patient_id
        }
    )


def get_doctor_patients(
    doctor_id
):

    return list(
        patients_collection.find(
            {
                "doctor_id": doctor_id
            }
        )
    )


def update_patient(
    patient_id,
    update_data
):

    return patients_collection.update_one(
        {
            "patient_id": patient_id
        },
        {
            "$set": update_data
        }
    )