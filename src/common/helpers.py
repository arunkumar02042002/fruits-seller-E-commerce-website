def validation_error_handler(errors: dict):
    """
    Function that takes errors dictionary from the serializers and
    returns the first error of the first key.
    """

    if isinstance(errors, list):
        error = errors[0]
        if isinstance(error, dict):
            key = list(error.keys())[0]
            message = error[key]
        else:
            message = error
        return message

    key = list(errors.keys())[0]
    error = errors[key]

    if type(error) == list:
        message = f"{key}: {error[0]}"
    else:
        message = f"{key}: {error}"
    return message
