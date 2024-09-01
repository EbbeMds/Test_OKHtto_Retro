from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()


# Data model
class Item(BaseModel):
    id: int
    name: str
    description: str


# File path to store JSON data
DATA_FILE = Path("data.json")

# Initialize the JSON file if it doesn't exist
if not DATA_FILE.exists():
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


# GET method to retrieve items
@app.get("/items/")
def get_items():
    with open(DATA_FILE, "r") as f:
        items = json.load(f)
    return items


# POST method to add an item
@app.post("/items/")
def add_item(item: Item):
    with open(DATA_FILE, "r") as f:
        items = json.load(f)

    # Check for duplicate ID
    if any(existing_item["id"] == item.id for existing_item in items):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")

    # Add the new item
    items.append(item.dict())
    with open(DATA_FILE, "w") as f:
        json.dump(items, f)
    return {"message": "Item added successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
