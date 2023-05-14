from fastapi import FastAPI, Path, Query, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str]


class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.get("/")
def home():
    return {"Data": "Test"}


@app.get("/about")
def about():
    return {"Data": "About"}


inventory = {}
#     1:{"name":"un nume", "price":10, "brand":"a brand"},

#  2:{
#     "name": "yuyu",
#     "price": 50,
#     "brand": "yuyutre"
#     }


# @app.get("/get-item/{item_id}")
# async def get_item(item_id:int):
#     return inventory[item_id]


@app.get("/get-items")
def get_items():
    for item_id in inventory:
        return inventory[item_id]


@app.get("/get-item/{item_id}")
async def get_item(item_id: int):
    # return inventory[item_id]
    #   for itemm_id in inventory:
    #     if itemm_id == item_id:
    return inventory[item_id]


# @app.get("/get-item/{item_id}")
# def get_item(item_id: int = Path(description="the id of the item you would like to see")):
#     return inventory[item_id]


@app.get("/get-by-name")
# def get_item(name:Optional[str]= None):
def get_item(name: str = Query(None, title="Name", description="Name of item.", max_length=10, min_length=2)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    # return {"Data": "Not found"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Item name not found")


@app.get("/get-by-name/{item_id}")
def get_item(item_id: int, name: Optional[str] = None):
    for item_id in inventory:
        if inventory[item_id]["name"] == name:
            return inventory[item_id]
    return {"Data": "Not found"}

# ==========================================
# ==========================================


@app.post("/create-item/{item_id}")
def create_item(item_id: str, item: UpdateItem):
    if item_id in inventory:
        return {"Error": "Item id already exists"}
    inventory[item_id] = item
    return inventory[item_id]


# ==========================================
# ==========================================

@app.put("/update-item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        return {"Error": "Item Id does not exist"}
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand

    inventory[item_id].update(item)
    return inventory[item_id]


# ==========================================
# ==========================================

@app.delete("/delete-item")
def delete_item(item_id: int = Query(..., description="The id of the item ")):
    if item_id not in inventory:
        return {"Error": "Id does not exist"}
    del inventory[item_id]
    return {"Success": "Item was deleted"}
