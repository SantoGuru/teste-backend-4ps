from pydantic import BaseModel
from typing import Optional

class CompanyCreateRequest(BaseModel):
    company_name: str
    cnpj: Optional[str] = None

class CompanyCreatedResponse(BaseModel):
    company_id: str
    message: str