# app/routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import schemas, crud, database, auth

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if crud.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    return user

@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = auth.create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserOut)
def me(current_user = Depends(auth.get_current_user)):
    return current_user
