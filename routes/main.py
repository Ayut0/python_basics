from fastapi import FastAPI, HTTPException
from typing import Union
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


items = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q:Union[str, None] = None):
#     return {"item_id":item_id, "q":q}

@app.get("/items/{item_id}")
def get_item(item_id: int) -> str:
    if item_id < len(items):
        return items[item_id]
    else:
        raise HTTPException(status_code=404, detail="Items not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name" : item.name, "item_id": item_id }

