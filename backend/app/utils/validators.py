import re

#Definindo função para normalizar telefone no formato brasileiro
def normalize_phone_br(v: str) -> str:
    # v= "+55 (011) 9 8765-4321"
    #Remove todos os caracteres não numéricos e espaços vazios
    s= re.sub(r"\D", "", str(v or ""))
    # Pós filtro: s="55011987654321"

    #Se o S estiver vazio, lança um erro de valor
    if not s:
        raise ValueError("telefone vazio.")
    #Remove o código do país, se presente
    if s.startswith("0055"):
        local = s[4:]
    elif s.startswith("55"):
        local = s[2:]
    else:
        local=s
    # Pós filtro: s="011987654321"

    #Remove o zero à esquerda do código de área, se presente
    if local.startswith("0") and len(local) in (11, 12):
        cand=local[1:]
        if len(cand) in (10, 11):
            local=cand
    # Pós filtro: s="11987654321"

    #Verifica se o telefone contém apenas 10 ou 11 dígitos
    if len(local) not in (10, 11):
        raise ValueError("telefone BR inválido: use DDD + número (10 ou 11 dígitos).")
    #+55 é adicionado ao início do número
    return "+55" + local