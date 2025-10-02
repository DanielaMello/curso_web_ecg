import os
import datetime as datetime
import jwt
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"
#definindo prazo de expiração do token em minutos
ACESS_TOKEN_EXPIRE_MINUTES = 60 #1 hora

#função para gerar o hash da senha (criptografar a senha)
def hash_password(password: str) -> str:
    return password_context.hash(password)

#função para verificar se a senha está correta (descriptografa e compara com a senha digitada)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

#função para criar o token de acesso
def create_access_token(subject: dict, minutes: int | None = None) -> str:
    exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=minutes or ACESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"exp": exp, "sub": subject}, SECRET_KEY, algorithm=ALGORITHM)

#funcao para decodificar o token de acesso
def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])