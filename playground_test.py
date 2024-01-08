from configparser import ConfigParser


cfg = ConfigParser()
cfg.read(r"configs\email\config.cfg")
print(cfg.get("ResetMail", "password"))
