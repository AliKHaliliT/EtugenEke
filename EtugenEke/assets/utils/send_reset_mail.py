from .load_conf import load_conf
from email.mime.multipart import MIMEMultipart
from .get_machine_ip import NetworkConfigFetcher
from email.mime.text import MIMEText
import smtplib


config = load_conf(r"E:\Ongoing\Python\EtugenEke\configs\email\config.cfg")
ncf = NetworkConfigFetcher()


def send(email: str, reset_token: str) -> None:

    """
    
    Sends a password reset link to the user's email.


    Parameters:
    -----------
    email : str
        The user's email address.


    Returns:
    --------
    None.
    
    """

    if not isinstance(email, str):
        raise TypeError("email must be a string")
    if not isinstance(reset_token, str):
        raise TypeError("reset_token must be a string")


    message = MIMEMultipart("alternative")

    message["Subject"] = "Password Reset"
    message["From"] = config.get("ResetMail", "email")
    message["To"] = email

    # This part is only for development purposes. You should add your own ip address here on production.
    # When broadcasting the server, the ip will be different based on the machine 
    # it is being broadcasted from. Thus it is tricky to hardcode the ip address.
    # The following code is used to get the ip address of the machine that is broadcasting the server.
    # The ip address is used to generate the reset link.
    # Note that the ip address being used is the ip address of the ethernet interface, so you might need to change
    # this part. That being said, this part is coded to take into account both windows and linux machines.
    for interface in ncf.fetch_network_config():
        if interface["Interface"] == "Ethernet" or interface["Interface"] == "eth0":
            reset_link = f"http://{interface['Address']}:8000/pages/user_action?token={reset_token}"
            break


    # Email body with the reset link
    text = f"Click the link below to reset your password:\n{reset_link}"
    html = f"""
    <html>
      <body>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
      </body>
    </html>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:

            server.starttls()
            server.login(config.get("ResetMail", "email"), config.get("ResetMail", "password"))
            server.sendmail(config.get("ResetMail", "email"), email, message.as_string())

    except Exception as e:
        print(f"Error in send: {e}")