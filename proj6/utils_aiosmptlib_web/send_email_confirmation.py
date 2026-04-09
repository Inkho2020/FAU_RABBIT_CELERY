from textwrap import dedent

from core import User
from utils_aiosmptlib_web.send_email import send_new_email
from utils_aiosmptlib_web.web_templates import templates


async def send_email_confirmation(
    user: User,
):
    recipient = user.email
    subject = "Email confirmed"
    plain_content = dedent(f"""\
        Dear {recipient},
        
       Your email address was confirmed.       
        
        Your WOHUS,  
        """)
    template = templates.get_template("confirm_email_verification.html")
    context = {
        "user": user,
    }
    html_content = template.render(context)
    await send_new_email(
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
        html_content=html_content,
    )
