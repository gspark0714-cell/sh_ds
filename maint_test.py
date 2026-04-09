from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "안녕하세요! FastAPI 작동 중입니다."}

@app.get("/hello/{name}")
def say_hello(name: str):
    return {"message": f"{name}님, 환영합니다!"}