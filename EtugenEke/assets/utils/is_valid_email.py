import re


def is_valid_email(email: str) -> bool:

    """
    
    This function checks if an email address is valid.


    Parameters
    ----------
    email : str
        The email address to check.

    
    Returns
    -------
    bool
        True if the email address is valid, False otherwise.
    
    
    """

    if not isinstance(email, str):
        raise TypeError("email must be a string")


    email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return bool(re.match(email_pattern, email))