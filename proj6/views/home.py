from typing import Annotated

from fastapi import APIRouter, Request, Depends

from core import User
from core.authentication.fau import current_active_user
from utils_aiosmptlib_web.web_template import templates

router = APIRouter(prefix="/home", tags=["HOMEPAGE"])


@router.get(
    "/",
    include_in_schema=True,
    name="home",
)
def home(
    request: Request,
    user: Annotated[User, Depends(current_active_user)],
):
    print(type(user), user)
    return templates.TemplateResponse(
        name="homepage.html",
        context={"request": request, "user": user},
        request=request,
    )
