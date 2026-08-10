# pyrefly: ignore [missing-import]
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello ():
    return {"Message" : "Hello Buddy"}

@app.get("/about")
def msg ():
    return {"Message" : "I am going to get a high paying job in next 2 months"}
