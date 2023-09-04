from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine
from typing import Annotated
from pydantic import BaseModel

SECRET_KEY = "0n1d3v"
EXPIRES_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
  db: Session = SessionLocal()
  try:
    return db
  finally:
    db.close()
    

def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
  return pwd_context.hash(password)


def authenticate(email: str, password: str, db: Session):
  user = db.query(models.Dev).filter(models.Dev.email == email).first()
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.utcnow() + expires_delta
  else:
    expire = datetime.utcnow() + timedelta(minutes=15)
  
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
  return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(username=email)
    except JWTError:
        raise credentials_exception
    user = db.query(models.Dev).filter(models.Dev.email == token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[models.Dev, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/")
def hu():
  return {"msg": "Hello world!"}

@app.get("/meal")
def calculate_meal_fee(beef_price: int, meal_price: int) -> int:
  total_price: int = beef_price + meal_price
  return total_price

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}