def validation_error_handler(errors: dict):
    """
    Function that takes errors dictionary from the serializers and
    returns the first error of the first key.
    """
    key = list(errors.keys())[0]
    error = errors[key]

    if type(error) == list:
        message = f"{key}: {error[0]}"
    else:
        message = f"{key}: {error}"
    return message
