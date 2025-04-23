from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, services
from ..dependencies import get_db

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=schemas.Response[schemas.UserOut], status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    try: user = services.register_user(db, user_in)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))
    return schemas.Response(status="success", message="User registered", data=user)

@router.post("/login", response_model=schemas.Response[schemas.Token])
def login(form_data: schemas.LoginForm, db: Session = Depends(get_db)):
    try: token = services.login_user(db, form_data)
    except ValueError as e: raise HTTPException(status_code=401, detail=str(e))
    return schemas.Response(status="success", message="Login successful", data={"access_token":token, "token_type":"bearer"})
