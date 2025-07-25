import uvicorn
from fastapi import FastAPI, Query
import requests
from typing import Annotated

app = FastAPI()

@app.get("/users")
async def root(nome: Annotated[str, Query(min_length=3)]):
    response = requests.get(f"http://flask-api:5000/get_data?nome={nome}")
    data = response.json()
    return {"message": data}

if __name__ == '__main__':
    uvicorn.run(host="0.0.0.0", port="8000")


# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}