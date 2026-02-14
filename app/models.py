
from sqlalchemy import Column , Integer , String , Boolean , TIMESTAMP , text , ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer , primary_key= True , nullable= False )
    title = Column(String , nullable= False)
    content = Column(String , nullable= False)
    activaties = Column(String)
    published = Column(Boolean , default= True , nullable= True)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    owner_id = Column(Integer , ForeignKey("users.id" , ondelete= "CASCADE") , nullable= False) 
    owner = relationship("User")
  
    
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer , primary_key= True , nullable= False)
    email = Column(String , nullable= False , unique = True)
    password = Column(String , nullable = False)
    created_at = Column(TIMESTAMP(timezone=True) , nullable=False , server_default=text('now()'))
    
    
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer , ForeignKey("users.id" , ondelete="CASCADE") , primary_key= True)
    post_id = Column(Integer , ForeignKey("posts.id" , ondelete="CASCADE") , primary_key= True)
    #vote_up
    #vote_down
    #maybe it should not be in the class vote but in the schemas and in the router of voting.....idk really
    
    
    
    
     
    