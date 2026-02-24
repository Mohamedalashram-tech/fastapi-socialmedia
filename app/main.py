from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from. import models
from .database import engine
from .routers import post, user , auth , vote
from .config import settings

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
    conn.commit()



#models.Base.metadata.create_all(bind=engine)
origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "The rooooooot"}
 