import uvicorn
from app_run import run
from api import router as api_router

app = run()

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
