def generate(error_message):
    """Generate an error message to be shown when a request is malformed

    Args:
        error_message (str): the specific error message

    Returns:
        str: the full error message including link to landing page
    """

    return f"{error_message} If you came here by accident, click <a href=\"/\">here</a> to generate a new calendar."