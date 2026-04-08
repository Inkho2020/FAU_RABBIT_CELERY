import uvicorn
import taskiq_fastapi
from app_run import run
from api import router as api_router
from core import broker

app = run()

taskiq_fastapi.init(broker, "main:app")

app.include_router(api_router)


@app.get("/")
def index():
    return {"message": "Hello email"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
        reload=True,
    )
