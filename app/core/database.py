from supabase import create_client, Client
from app.core.config import settings

# Cliente Público (Usa a chave anon - Sujeito às regras de segurança RLS)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Cliente Admin (Usa a chave service_role - IGNORA O RLS)
if not settings.SUPABASE_SERVICE_ROLE_KEY:
    raise ValueError("⚠️ SUPABASE_SERVICE_ROLE_KEY não encontrada no .env!")

supabase_admin: Client = create_client(
    settings.SUPABASE_URL, 
    settings.SUPABASE_SERVICE_ROLE_KEY
)