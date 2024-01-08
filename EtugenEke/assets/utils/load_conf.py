from configparser import ConfigParser


def load_conf(path: str = "config.cfg") -> dict[str, str]:

    """
    
    Load configuration from config.cfg

    
    Parameters
    ----------
    None.


    Returns
    -------
    config : dict
        Configuration from config.cfg

    """

    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not path.endswith(".cfg"):
        raise ValueError("path must point to a config file")
    

    try:
        with open(path) as config_file:
            cfg = ConfigParser()
            return cfg.read(config_file)
    except Exception as e:
        print("Please create a valid config.cfg file. Cuurently, you are receiving the error:", e)
        exit()