from database.mongodb import (
    consultations_collection
)


def create_consultation(data):

    return consultations_collection.insert_one(
        data
    )


def get_consultation(
    consultation_id
):

    return consultations_collection.find_one(
        {
            "consultation_id":
            consultation_id
        }
    )


def get_doctor_consultations(
    doctor_id
):

    return list(
        consultations_collection.find(
            {
                "doctor_id":
                doctor_id
            }
        )
    )


def update_consultation(
    consultation_id,
    update_data
):

    return consultations_collection.update_one(
        {
            "consultation_id":
            consultation_id
        },
        {
            "$set":
            update_data
        }
    )