from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import select, Session
from app.schemas import user, token
from app.db.engine import get_db
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token

router = APIRouter()


@router.post("/login", response_model=token.TokenResponse)
def login(user_data: user.UserLogin, session: Session = Depends(get_db)):
    user = session.exec(
        select(User).where(User.email == user_data.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")

    check_password = verify_password(
        user_data.password, user.password)
    if not check_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    token = create_access_token(
        user.name, user.email, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: user.UserCreate, session: Session = Depends(get_db)):
    existing_email = session.exec(
        select(User).where(User.email == user_data.email))
    if existing_email.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(name=user_data.name,
                    email=user_data.email, password=hashed_pwd)
    session.add(new_user)
    session.commit()

    return {"message": "Registration successful"}
