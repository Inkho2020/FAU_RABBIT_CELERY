from textwrap import dedent

from core import User
from utils_email_jinja.send_email import send_new_email
from utils_email_jinja.web_template import templates


async def send_verification_email(
    user: User,
    verification_link: str,
    # verification_token: str,
):
    recipient = user.email
    subject = "Confirm your registration"
    plain_content = dedent(f"""\
        Dear {recipient},
        
        Please follow the link to veriry your email.
        {verification_link}
        
        Your WOHUS,  
        """)
    #
    # User this code to verify you email:
    # {verification_token}
    template = templates.get_template("get_email_verification.html")
    context = {
        "user": user,
        "verification_link": verification_link,
        # "verification_token": verifcation_token,
    }
    html_content = template.render(context)
    await send_new_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
