from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from pydantic import BaseModel

app = FastAPI()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)


cursor = db.cursor()


origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Item(BaseModel):
    name: str

@app.get("/items", tags=["items"])
def read_items():
    try:
        cursor.execute("SELECT * FROM items")
        items = [{"id": row[0], "name": row[1]} for row in cursor.fetchall()]
        return items
    except:
        raise HTTPException(status_code=500, detail="Database error")
    


@app.post("/items", response_model=Item)
def create_item(item: Item):
    try:
        query = "INSERT INTO items (name) VALUES (%s)"
        cursor.execute(query, (item.name, ))
        db.commit()
        return {"name" : item.name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

@app.put("/items/{item_id}", response_model = Item)
def update_item(item_id: int, item: Item):
    try:
        query = "UPDATE items SET name = %s WHERE id = %s"
        cursor.execute(query, (item.name, item_id))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return { "id" : item_id, "name" : item.name }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    


@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    try:
        query = "DELETE FROM items WHERE id = %s"
        cursor.execute(query, (item_id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Item not found")
        return { "message" : "Item Deleted" }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    