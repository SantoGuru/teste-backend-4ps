from pydantic import BaseModel
from typing import Optional

class CompanyCreate(BaseModel):
    company_name: str
    cnpj: Optional[str] = None

class CompanySetupResponse(BaseModel):
    company_id: str
    message: str