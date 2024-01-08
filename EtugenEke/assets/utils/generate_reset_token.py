import secrets


def generate() -> str:

    """
    
    Generates a secret key for creating unique reset links.

    
    Parameters:
    -----------
    None.


    Returns:
    --------
    reset_token : str
        A secret key for creating unique reset links.

    """


    return secrets.token_urlsafe(32)