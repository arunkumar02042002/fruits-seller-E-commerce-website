from rest_framework import status
from rest_framework.response import Response


def reponse_200OK(message=None, payload=None):
    """Send a custom 200 Response"""
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

def reponse_201Created(message=None, payload=None):
    """Send a custom 201 Response"""
    if message is None: message = "Data created successfully."

    response = Response(
        {
            "status" : "success",
            "message" : message,
            "payload" : payload
        },
        status=status.HTTP_201_CREATED
    )

    return response

def response_204NoContent(message=None, payload=None):
    """Send a custom 204 Response"""
    if message is None: message = "No content found."

    response = Response(
        {
            "status" : "success",
            "message" : message,
            "payload" : payload
        },
        status=status.HTTP_204_NO_CONTENT
    )

    return response
