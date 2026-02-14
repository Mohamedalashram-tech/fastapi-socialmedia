from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List , Optional
from sqlalchemy import func


from .. import models
from .. import schemas
from .. import database
from .. import oauth2

router = APIRouter(
    prefix="/posts", 
    tags=['Posts']    
)

@router.get("/", response_model=List[schemas.PostVote])
def get_posts(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user) , limit : int = 5 , skip : int = 0 , search : Optional[str] = ""): 
    print(limit)
    
   
    
    posts = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts






@router.get("/mine", response_model=List[schemas.Post])
def get_my_posts(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
   
    print(current_user.email) 
    
    new_post = models.Post( owner_id = current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post

@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post , func.count(models.Vote.post_id).label("votes")).join(models.Vote , models.Vote.post_id == models.Post.id , isouter= True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post



@router.get("/user/{id}", response_model=List[schemas.Post])
def get_posts_by_user(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).filter(models.Post.owner_id == id).all()
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"No posts found for user with id: {id}")
    return posts


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.UbdatePost, db: Session = Depends(database.get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail=f"not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(post) 
    
    return post