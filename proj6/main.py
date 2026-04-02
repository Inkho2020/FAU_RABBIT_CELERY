import uvicorn
from app_run import run

app = run()


@app.get("/")
def index():
    return {"message": "Hello email"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="localhost",
        port=8001,
    )
