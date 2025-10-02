from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.db_models import User
from backend.app.models.user import UserCreate, UserOut, UserLogin, TokenWithUser
from backend.app.utils.security import hash_password
from backend.app.services.auth_user import authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    name_norm = payload.name.strip()
    email_norm = payload.email
    phone_norm = payload.phone

    #Validação para verificar se o e-mail ou telefone já existe no banco de dados
    exists = db.query(User).filter(
        or_(
            func.lower(User.name) == name_norm.lower(),
            func.lower(User.email) == email_norm.lower(),
            User.phone == phone_norm,
        )
    ).first()

    #Caso exista no banco:
    if exists:
        raise HTTPException(status_code=409, detail="username/email/phone já cadastrado")

    #Caso não exista, cria o usuário
    user = User(
        name=name_norm,
        email=email_norm,
        phone=phone_norm,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return 

#método e conexão com o banco
@router.post("/login", response_model=UserOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, payload)

        #se der certo, retorna o token e os dados do usuário
        return user
    
    #se der errado, retorna erro 401
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))