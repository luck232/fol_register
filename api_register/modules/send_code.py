import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def verify(new_user_email: str, public_code:str, smtp_server:str, smtp_port:int, smtp_user:str, smtp_password:str):
    smtp_server = smtp_server
    port = smtp_port
    sender_email = smtp_user
    password = smtp_password
    subject = "verify you account"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = new_user_email
    message["Subject"] = subject
    message.attach(MIMEText(f"create your account http://127.0.0.1:5000/confirm?pu_code={public_code}", "plain"))


    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, new_user_email, message.as_string())

