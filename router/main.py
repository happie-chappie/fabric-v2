from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize FastAPI app
app = FastAPI(
    title="Router API",
    description="A basic FastAPI application with GET and POST routes",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """Health check endpoint for Fly.io"""
    return {"status": "healthy"}

# Pydantic model for our data
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# In-memory storage
items: List[Item] = []
current_id = 1

@app.get("/")
async def root():
    """Root endpoint returning a welcome message"""
    return {"message": "Welcome to the Router API"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """Get all items"""
    return items

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get a specific item by ID"""
    item = next((item for item in items if item.id == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=201)
async def create_item(item: Item):
    """Create a new item"""
    global current_id
    
    # Assign an ID to the new item
    item.id = current_id
    current_id += 1
    
    items.append(item)
    return item