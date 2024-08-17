from email.message import EmailMessage
import ssl
import smtplib

email_sender = ""
email_password = ""


def send_mail(subject, receiver_email, password):

    body = f"""
        Your password is {password}
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver_email
    em['subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver_email, em.as_string())