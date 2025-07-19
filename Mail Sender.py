import smtplib
from email.mime.text import MIMEText

def send_email_smtplib():
    sender = "zzezzo424@gmail.com"
    password = "your_app_password_here"  # Use app-specific password
    recipient = "aaoaao424@gmail.com"
    
    msg = MIMEText("Hello, this is a reminder about our Iftar date on DATE. See you there!")
    msg['Subject'] = 'Iftar reminder'
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)

if __name__ == "__main__":
    send_email_smtplib()