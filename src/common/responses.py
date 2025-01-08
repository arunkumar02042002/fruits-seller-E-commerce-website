from rest_framework import status
from rest_framework.response import Response


def reponse_200OK(message=None, payload=None):
    """Send a custom Response"""
    if message is None: message = "Data retreived successfully."

    response = Response(
        {
            "status" : "success",
            "message" : message,
            "payload" : payload
        },
        status=status.HTTP_200_OK
    )

    return response
