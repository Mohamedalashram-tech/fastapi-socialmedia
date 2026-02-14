from jose import JWTError , jwt
from datetime import timedelta , datetime , timezone
from fastapi import Depends , status , HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .schemas import TokenData
from .database import  get_db
from .models import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#SECRET_Key
#Algorithm
#Expriation time

SECRET_Key = settings.secret_key
#It should be a long complicated secret key

Algorithm = settings.algorithm

ACCESS_TOKEN_MINUTES = settings.access_token_expire_minutes

def create_Access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    
    to_encode.update({"exp" : expire})
    
    encoded_jwt = jwt.encode(to_encode , SECRET_Key , algorithm= Algorithm)
    
    return encoded_jwt    


def verify_Access_token(token:str , credentials_exception):
    
    try:
        payload = jwt.decode(token , SECRET_Key , algorithms = Algorithm)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
    
    
 
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    
    token_data = verify_Access_token(token, credentials_exception)


    user = db.query(User).filter(User.id == token_data.id).first()

    return user
