from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.database import supabase, supabase_admin

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica o token JWT enviado no cabeçalho.
    Se for válido, retorna os dados do usuário logado.
    Se for inválido, bloqueia a requisição (401).
    """
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        
        if not user_response or not user_response.user:
            raise HTTPException(
                status_code=401,
                detail="Token inválido, expirado ou usuário não encontrado.",
            )
        
        return user_response.user
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Credenciais inválidas.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

def verify_company_access(company_id: str, user_id: str):
    """
    Verifica no banco se o usuário tem vínculo ativo com a empresa.
    Se não tiver, levanta um erro 403 e trava a requisição.
    """
    link = supabase_admin.table("user_company_links") \
        .select("id") \
        .eq("user_id", user_id) \
        .eq("company_id", company_id) \
        .eq("is_active", True) \
        .execute()
        
    if not link.data:
        raise HTTPException(
            status_code=403, 
            detail="Você não tem permissão para operar nesta empresa."
        )
    return True