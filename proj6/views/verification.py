from fastapi import APIRouter, Request

from utils_aiosmptlib_web.web_template import templates

router = APIRouter(
    prefix="/verify-email",
    tags=["Verify"],
)


@router.get(
    "/",
    include_in_schema=True,
    name="verify-email",
)
def verify_email(
    request: Request,
):
    return templates.TemplateResponse(
        name="verification.html",
        context={
            "request": request,
        },
        request=request,
    )
