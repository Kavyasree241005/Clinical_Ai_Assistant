from database.mongodb import (
    reports_collection
)


def create_report(data):

    return reports_collection.insert_one(
        data
    )


def get_report(
    report_id
):

    return reports_collection.find_one(
        {
            "report_id":
            report_id
        }
    )


def get_doctor_reports(
    doctor_id
):

    return list(
        reports_collection.find(
            {
                "doctor_id":
                doctor_id
            }
        )
    )


def finalize_report(
    report_id
):

    return reports_collection.update_one(
        {
            "report_id":
            report_id
        },
        {
            "$set":
            {
                "finalized": True
            }
        }
    )