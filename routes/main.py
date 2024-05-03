from fastapi import FastAPI, HTTPException, Query, Path, Body
from typing import Union, Annotated, List
from pydantic import BaseModel, Field, HttpUrl
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


items = []
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/")
def read_root():
    return {"Hello": "World"}

# query params
# http://127.0.0.1:8000/items/?skip=0&limit=10
# @app.get("/items")
# async def read_item(skip: int = 0, limit: int=10):
#     return fake_items_db[skip: skip + limit]

@app.get("/items/")
async def read_item(q: Annotated[str, Query(title="Query string", description="The description allows us to put an explanation about a query", min_length= 3, deprecated=True)]):
    results = {"items" : [{"item_id" : "Foo"}, {"item_id" : "Bar"}]}
    if q:
        results.update({"q": q})

    return results

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
def create_item(item:Item):
    items.append(item)
    return items

# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
#     results = {"item_id": item_id, "item": item, "user": user}
#     return results

# Embed a single body parameter
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Annotated[Item, Body(embed=True)]):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer

@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images