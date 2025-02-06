from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Привет это мой первый FastAPI сервер!"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
