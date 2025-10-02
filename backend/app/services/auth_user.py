from backend.app.models.user import UserLogin
from backend.app.db_models import User
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.app.utils.security import verify_password, create_access_token

#verifica se o usuário existe pelo e-mail e se a senha está correta
def authenticate_user(db:Session, payload: UserLogin) -> tuple[User, str]:
    #retira os espaços vazios do início e do fim
    ident = payload.email.strip()
    query = db.query(User)
    #pega todas as informações do usuário pelo e-mail, ignorando maiúsculas e minúsculas
    user = query.filter(func.lower(User.email) == ident.lower()).first()
    #retorna erro caso usuário não exista
    if not user:
        raise ValueError("Usuário não encontrado")
    
    #verificar se senha está correta comparando com o hash armazenado
    if not verify_password(payload.password, user.password_hash):
        raise ValueError("Senha incorreta")
    
    #gerar o token de acesso JWT
    token = create_access_token({"sub": str(user.id), "name": user.name, "email": user.email})
    return user
