from email.message import EmailMessage
from email.mime.text import MIMEText

import aiosmtplib


async def send_email(
    recipient: str,
    subject: str,
    body: str,
):
    admin_email = "no_reply@newsletter.com"

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="localhost",
        port=1025,
    )


async def send_new_email(
    recipient: str,
    subject: str,
    plain_content: str,
    html_content: str = "",
):
    admin_email = "confirm@wohus.com"

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(plain_content)
    if html_content:
        message.add_alternative(
            html_content,
            subtype="html",
        )
    # plain_message = MIMEText(
    #     plain_content,
    #     "plain",
    #     "utf-8",
    # )
    # message.attach(plain_message)
    # if html_content:
    #     html_message = MIMEText(
    #         html_content,
    #         "html",
    #         "utf-8",
    #     )
    #     message.attach(html_message)

    await aiosmtplib.send(
        message,
        sender=admin_email,
        recipients=[recipient],
        hostname="localhost",
        port=1025,
    )
