from configparser import ConfigParser


def load_conf(path: str = "config.cfg") -> ConfigParser:

    """
    
    Load configuration from `config.cfg`

    
    Parameters
    ----------
    path : str
        Path to the configuration file. The default value is `config.cfg`


    Returns
    -------
    config : dict
        Configuration from `config.cfg`

    """

    if not isinstance(path, str):
        raise TypeError("path must be a string")
    if not path.endswith(".cfg"):
        raise ValueError("path must point to a config file")
    

    try:
        cfg = ConfigParser() 
        cfg.read(path)


        return cfg
    except Exception as e:
        print("Please create a valid config.cfg file. Cuurently, you are receiving the error:", e)
        exit()