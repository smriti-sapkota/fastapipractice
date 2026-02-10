from fastapi import FastAPI, Body , HTTPException , status , Response
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi',user='postgres', password='5555', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection with Database was Successful")
        break
    
    except Exception as error:
        print("Connecting to database failed")
        print("Error:", error)
        time.sleep(2)
       
    
     

# my_posts = [{"title":"Books", "content":"Book thief", "id":1},
#             {"title":"Flower", "content":"SuryaMukhi", "id":2},
#             {"title":"Mountains", "content":"Mardi", "id":3},
#             {"title":"Location", "content":"Chitwan", "id":4}]

class Post(BaseModel):
    title : str
    content : str
    published : bool = True

# def find_post(id):
#     for p in my_posts:
#         if p["id"]==id:
#             return p
        

# def find_index_post(id):
#     for i , p in enumerate(my_posts):
#        if p["id"]==id:
#            return i
           

@app.get("/")
def root():
    return{"messsge":"Hii Baddieji"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"All posts": posts}
    # cursor.execute("""SELECT * FROM Posts """)
    # posts = cursor.fetchall()
    # print(posts)
    # return{"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):

    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s, %s, %s) RETURNING * """,(post.title,post.content,post.published))
    new_post = cursor.fetchone() #* bata return vako value store hunxa
    conn.commit()
    # post_dict["id"] = randrange(0,1000000)
    # my_posts.append(post_dict)
    return{"data" : new_post}

@app.get("/posts/{id}")
def retrieve_posts(id : int):
    cursor.execute(f"""SELECT * FROM posts WHERE id={id} """)

    post = cursor.fetchone()
  
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"post with id {id} not found" )
    
    return{"data" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id : int):
    cursor.execute(f"""DELETE FROM posts WHERE id={id} RETURNING *""")
    


    deletedPost = cursor.fetchone()


    if deletedPost==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"post with id{id} not found" )
    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_posts(id : int , post : Post):
     cursor.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
     updated_posts = cursor.fetchone()

     if updated_posts==None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND , detail=f"{id} not found" )
     
     conn.commit()

     return{"data" : updated_posts}

    





