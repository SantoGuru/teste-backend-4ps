from fastapi import APIRouter, HTTPException, Depends
from app.schemas.onboarding import CompanyCreateRequest, CompanyCreatedResponse
from app.services.setup_company import setup_new_company
from app.core.security import get_current_user
from app.core.database import supabase 

router = APIRouter()

@router.post("/onboarding", response_model=CompanyCreatedResponse, status_code=201)
def create_first_company(
    payload: CompanyCreateRequest, 
    current_user = Depends(get_current_user)
):
    try:
        new_id = setup_new_company(
            user_id=current_user.id, 
            company_name=payload.company_name,
            cnpj=payload.cnpj
        )
        return {"company_id": new_id, "message": "Ecossistema da empresa criado com sucesso!"}
    except Exception as e:
        print(f"Erro Onboarding: {e}")
        raise HTTPException(status_code=500, detail=str(e))