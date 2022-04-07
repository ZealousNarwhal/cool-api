from fastapi import FastAPI
from fastapi import status, Response
from pydantic import BaseModel
import time
import psycopg
from psycopg.rows import dict_row
from settings.config import settings

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

def CheckPost(post, response):
    if post:
        return post
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return "404: Not Found"

while True:
    try:
        conn = psycopg.connect(
            dbname = settings.db_name,
            user = settings.db_user,
            password = settings.db_password,
            port = settings.db_port,
            host = settings.db_host,
            row_factory=dict_row,
        )
        cursor = conn.cursor()
        break
    except Exception as error:
        print("Error connecting to PostgreSQL")
        print(error)
        time.sleep(5)


@app.get("/")
async def root():
    return {"message": "This is a test API to communicate to a PostgreSQL database."}


@app.get("/posts")
async def root():
    cursor.execute("SELECT * FROM fastapi_test")
    posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}")
async def root(id: int, response: Response):
    cursor.execute("SELECT * FROM fastapi_test WHERE post_id = %s", 
    (str(id),))
    post = cursor.fetchone()
    return CheckPost(post, response)


@app.post("/posts", status_code=status.HTTP_201_CREATED )
async def root(data: Post):
    cursor.execute("INSERT INTO fastapi_test (title, content, published) VALUES (%s, %s, %b) RETURNING * ", 
    (data.title, data.content, data.published))
    post = cursor.fetchone()
    conn.commit()
    return post


@app.put("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def root(id:int, data: Post, response: Response):
    cursor.execute("UPDATE fastapi_test SET title = %s, content = %s, published = %b WHERE post_id = %s RETURNING *", 
    (data.title, data.content, data.published, str(id)))
    post = cursor.fetchone()
    conn.commit()
    return CheckPost(post, response)


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def root(id: int, response: Response):
    cursor.execute("DELETE FROM fastapi_test WHERE post_id = %s RETURNING *", (str(id),))
    post = cursor.fetchone()
    conn.commit()
    return CheckPost(post, response)