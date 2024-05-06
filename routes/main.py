from fastapi import FastAPI, HTTPException, Query, Path, Body, Cookie, Header, Response
from typing import Any, Union, Annotated, List
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field, HttpUrl, EmailStr
from enum import Enum


app = FastAPI()

class Image (BaseModel):
    url: HttpUrl
    name: str
class Item(BaseModel):
    name: str
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    description: str | None = Field(
        default = None, title = "The description of the item", max_length=300
    )
    tax: float | None = None
    tags: set[str] = []
    image: list[Image] | None = None

    model_config = {
        "json_schema_extra": {
            "examples" : [
                {
                    "name": "Foo",
                    "price": 35.4,
                    "description": "A very nice item",
                    "tax": 3.2,
                }
            ]
        }
    }

class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items : list[Item]

class User(BaseModel):
    username:str
    full_name: str | None = None

class ModelName(str, Enum):
    alexnet="alexnet"
    resnet="resnet"
    lenet="lenet"

class BaseUser(BaseModel):
    username:str
    email: EmailStr
    full_name: str | None = None

# Make sure not to user the same response to multiple endpoints
# UserInput inherits from BaseUser
class UserInput(BaseUser):
    password: str

class UserOutput(BaseModel):
    username: str
    email: str
    full_name: str | None = None

items = []
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# If you declare a response model, FastAPI will use it to validate the response data
# In other words, FastAPI prioritizes the response model over the return type annotation
@app.post("/users/")
async def create_user(user: UserInput) -> BaseUser:
    return user

@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://fastapi.tiangolo.com")
    return JSONResponse(content={"message": "Hello World"})

@app.get("/")
def read_root():
    return {"Hello": "World"}

# query params
# http://127.0.0.1:8000/items/?skip=0&limit=10
# @app.get("/items")
# async def read_item(skip: int = 0, limit: int=10):
#     return fake_items_db[skip: skip + limit]

# Annotated
# @app.get("/items/")
# async def read_item(q: Annotated[str, Query(title="Query string", description="The description allows us to put an explanation about a query", min_length= 3, deprecated=True)]):
#     results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
#     if q:
#         results.update({"q": q})

#     return results

# cookie
# @app.get("/items/")
# async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
#     return {"ads_id": ads_id}

# Header
@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

# http://localhost:8000/items/?q=foo&q=bar
# @app.get("/items/")
# async def read_items(q: Annotated[list[str] | None, Query()] = None):
#     query_items = {"q": q}
#     return query_items

@app.get("/items/{item_id}")
async def read_item(item_id: Annotated[str, "This is a metadata"], q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update({"description" : "This is an amazing item that has a long description"})
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: Annotated[int, Path(title='The ID of the user to get', ge=1)], item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id" : user_id}

    if q:
        item.update({"q" : q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})

# @app.get("/items/{item_id}", response_model=Item)
# def get_item(item_id: int) -> Item:
#     if item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    
    if model_name.value == "lenet":
        return {"model_name":model_name, "message": "LeCNN all the images"}
    
    return {"model_name": model_name, "message": "Have some residuals"}


@app.post("/items")
def create_item(item:Item) -> Item:
    items.append(item)
    return items

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results

# Embed a single body parameter
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(
    openapi_examples={
        "normal":{
            "summary": "A normal example",
            "description": "A normal description",
            "value":{
                "name": "Foo",
                "price": 35.4,
                "tax" : 3.2,
                "description": "A very nice item"
            },
        },
        "converted": {
            "summary" : "An example with converted data",
            "description": "FastAPI can covert price `settings to actual `number` automatically",
            "value":{
                "name": "Bar",
                "price": "35.4",
            },
        },
        "invalid" :{
            "summary": "An example with invalid data",
            "description": "FastAPI will return an error if the price is less than or equal to zero",
            "value":{
                "name": "Baz",
                "price": 0,
            },
        },
    }
)]):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images