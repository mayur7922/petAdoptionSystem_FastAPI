from fastapi import FastAPI # type: ignore

app = FastAPI()

@app.get("/")
def index():
    return {"data" : {"name" : "Mayur"}}
