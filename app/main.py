from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# allows https://www.google.com to fetch('http://localhost:8000/').then(res => res.json()).then(console.log)
# origins = ["https://www.google.com"]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World!!!"}


# my_posts: List[Dict] = []
#
#
# def find_post(id):
#     for post in my_posts:
#         if post['id'] == id:
#             return post
#
#
# def find_index_post(id):
#     for index, post in enumerate(my_posts):
#         if post['id'] == id:
#             return index
