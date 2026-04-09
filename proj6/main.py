import uvicorn
from fastapi import Request
import taskiq_fastapi
from utils_aiosmptlib_web.web_template import templates

from app_run import run
from api import router as api_router
from views import router as views_router
from core import broker

app = run()

taskiq_fastapi.init(broker, "main:app")

app.include_router(api_router)
app.include_router(views_router)


@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
    )
