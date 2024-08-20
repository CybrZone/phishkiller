# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# def read_root():
#     return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}



from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


class UserCreate(BaseModel):
    a: str
    az: str
    # username: str

@app.post("/create_user/")
async def create_user(user_data: UserCreate):
    email = user_data.a
    password = user_data.az

    f = open("log.txt", "a")
    f.write(f'[+] email: {email}, password: {password}\n')
    f.close()

    return {
        "msg": "we got data succesfully",
    }
 
 
if __name__ == "__main__":
    import uvicorn
 
    uvicorn.run(app, host="127.0.0.1", port=8000)
