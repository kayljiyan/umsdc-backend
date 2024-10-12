# pip install fastapi 'uvicorn[standard]'

# imports the fastapi class
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

# creates an instance of the FastAPI class and assigns it to the app variable
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# defines a route that responds to GET requests at the /hello/{name} endpoint
@app.get("/hello/{name}")
async def hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/tasks")
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    tasks = []
    for row in rows:
        tasks.append({"id": row[0], "title": row[1], "description": row[2]})

    conn.close()
    return tasks

@app.post("/task")
async def add_task(request: Request):
    payload = await request.json()
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    title = payload["title"]
    description = payload["description"]

    cursor.execute("INSERT INTO tasks (title, description) VALUES (?,?)", (title, description))
    conn.commit()
    conn.close()

    return {"message": "Task added successfully"}

@app.delete("/task/{id}")
async def delete_task(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return {"message": "Task deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
