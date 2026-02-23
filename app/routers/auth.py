
from fastapi import APIRouter ,Depends , status , Response , HTTPException
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#project imports
from ..database import get_db
from ..schemas import UserLogin , Token
from ..models import User
from ..utils import pwd_context , hash , verify
from ..oauth2 import create_Access_token



router = APIRouter(
    prefix='/login',
    tags=['Authentication']
    )

@router.post('/' , response_model= Token)
async def login( user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail=f"Invalid Credentials")

    if not verify(user_credentials.password , user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN , detail=f"Invalid Credentials")
   
    access_token =  create_Access_token(data = {"user_id": user.id})
    
    
    return {"access_token" : access_token , "token_type" : "bearer"}
    
    


