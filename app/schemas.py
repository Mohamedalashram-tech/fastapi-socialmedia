from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional
from enum import Enum


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    activaties: Optional[str] = None
    
class User_needed_information(BaseModel):
    email: EmailStr

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime
    
    class Config:
        from_attributes = True 
        

class CreatePost(PostBase):
    pass

class UbdatePost(PostBase):
    pass

class Post(PostBase): 
    
    created_at: datetime
    owner_id : int
    id: int
    owner : User_needed_information
    

    class Config:
        from_attributes = True
        


class PostVote(BaseModel): 
    Post: Post 
    votes: int

    class Config:
        from_attributes = True
        
         
class UserCreate(BaseModel):
    email:EmailStr
    password: str
    
    
class UserLogin(BaseModel):
    email : EmailStr
    password : str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
    
    
class VoteDirection(int, Enum):
    LIKE = 1
    DISLIKE = -1
    REMOVE = 0
    
class Vote(BaseModel):
    post_id: int
    dir: int