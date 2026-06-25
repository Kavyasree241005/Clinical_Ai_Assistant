from database.mongodb import doctors


def register_doctor(data):

    doctors.insert_one(data)


def get_doctor_by_email(email):

    return doctors.find_one(
        {
            "email": email
        }
    )


def login_doctor(
    email,
    password
):

    return doctors.find_one(
        {
            "email": email,
            "password": password
        }
    )