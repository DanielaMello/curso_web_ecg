#models verifica as informações que vem e trata elas para enviar
#user.py trata os dados verificando validação, encapsula em dicionário e envia pra proxima etapa
from typing_extensions import Annotated

from pydantic import BaseModel, Field, EmailStr
from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from backend.app.utils.validators import normalize_phone_br

#Validação do e-mail, tomo e-mail ficará em minúsculo antes de ser validado
EmailLower = Annotated[EmailStr, BeforeValidator(lambda v: str(v).lower())]
#Validação do telefone, o telefone será normalizado antes de ser validado
PhoneBR = Annotated[str, BeforeValidator(normalize_phone_br)]

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    #dados já vem após tratamento e normalização
    email: EmailLower
    phone: PhoneBR

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserOut(UserBase):
    id: int
    name: str
    email: EmailLower
    phone: PhoneBR      
    model_config = ConfigDict(from_attributes=True)