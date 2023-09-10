import uvicorn
from fastapi import FastAPI, Body, Depends

from app.auth.model import PostSchema, UserSchema, UserLoginSchema
from app.auth.jwt_handler import signJWT
from app.auth.jwt_bearer import jwtBearer

posts = [
    {
        "id": 1,
        "title": "penguins",
        "content": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "tigers",
        "content": "Tigers are the largest living cat species and a memebers of the genus Panthera."
    },
    {
        "id": 3,
        "title": "koalas",
        "content": "Koala is arboreal herbivorous marsupial native to Australia."
    },
]


users = []



app = FastAPI()

# Get - for testing
@app.get("/", tags=["test"])
def greet():
    return {"Hello":"World!"}


# Get Posts
@app.get("/posts", tags=["Posts"])
def get_posts():
    return {"data": posts}


# Get single post {id}
@app.get("/posts/{id}", tags=["Posts"])
def get_one_post(id: int):
    if id > len(posts):
        return {
            "error": "Post with this ID does not exists!"
        }
    for post in posts:
        if post["id"] == id:
            return {
                "data": post
            }
        
# Post a blog post [A handler for creating post]
@app.post("/posts", dependencies=[Depends(jwtBearer())], tags=["Posts"])
def add_post(post: PostSchema):
    post.id = len(posts)+1
    posts.append(post.dict())
    return {
        "info": "Post Added!"
    }




@app.get("/users", tags=["User"])
def user_list():
    return {
        "data": users
    }

# User SignUp [ Create a new user ]
@app.post("/user/signup", tags=["User"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False
    

@app.post("/user/login", tags=["User"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return signJWT(user.email)
    else:
        return {
            "error": "Invalid login details!"
        }