import base64


def tob64(path: str) -> str:

    """
    
    Given an image path, reads the image file and encodes it to base64.

    
    Parameters:
    -----------
    path : str
        The path to the image file.


    Returns:
    --------
    image : str
        The base64 encoded image.

    """

    if not isinstance(path, str):
        raise TypeError("Path must be a string")


    with open(path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode("utf-8")

    
    return image