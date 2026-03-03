from fastapi import FastAPI
from app.core.config import settings
from app.core.database import supabase

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/")
def root():
    return {"message": "API rodando! 🚀"}

@app.get("/health")
def health_check():
    try:
        response = supabase.table("companies").select("id").limit(1).execute()
        return {"status": "online 🟢", "database": "conectado", "data": response.data}
    except Exception as e:
        return {"status": "offline 🔴", "error": str(e)}