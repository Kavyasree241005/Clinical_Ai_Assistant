from database.mongodb import (
    voice_collection
)


def save_embedding(data):

    return voice_collection.insert_one(
        data
    )


def get_embedding(
    doctor_id
):

    return voice_collection.find_one(
        {
            "doctor_id":
            doctor_id
        }
    )


def update_embedding(
    doctor_id,
    embedding_path
):

    return voice_collection.update_one(
        {
            "doctor_id":
            doctor_id
        },
        {
            "$set":
            {
                "embedding_path":
                embedding_path
            }
        }
    )