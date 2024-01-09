# from configparser import ConfigParser


# cfg = ConfigParser()
# cfg.read(r"configs\email\config.cfg")
# print(type(cfg.get("ResetMail", "email")))

from EtugenEke.assets.utils.load_conf import load_conf


config = load_conf(r"E:\Ongoing\Python\EtugenEke\configs\email\config.cfg")

# Print out the values retrieved from the configuration file
print("Config Email:", repr(config.get("ResetMail", "email")))
print("Config Password:", repr(config.get("ResetMail", "password")))

# Rest of your code remains the same
