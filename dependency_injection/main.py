from typing import Annotated

from fastapi import FastAPI, Depends

app = FastAPI()


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100 ):
    return {"q": q, "skip": skip, "limit": limit}

# we can store value in a variable
# if we use Annotated
CommonDep = Annotated[dict, Depends(common_parameters)]

# we have to write the whole parameter with the type annotation and Depends()
@app.get("/items/")
async def read_items(commons: Annotated[dict, CommonDep]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, CommonDep]):
    return commons

