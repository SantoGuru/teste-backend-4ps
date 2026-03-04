from app.core.database import supabase_admin 

def setup_new_company(user_id: str, company_name: str, cnpj: str = None) -> str:
    """
    Cria a empresa e configura todo o ecossistema padrão 4Ps.
    """
    # 1. Cria a Empresa
    res_company = supabase_admin.table("companies").insert({
        "name": company_name,
        "cnpj": cnpj
    }).execute()
    new_company_id = res_company.data[0]['id']

    # 2. Cria Cargos Base
    res_role = supabase_admin.table("app_roles").insert({
        "company_id": new_company_id,
        "name": "Administrador",
        "description": "Acesso total ao sistema",
        "is_system_role": True
    }).execute()
    owner_role_id = res_role.data[0]['id']

    supabase_admin.table("app_roles").insert({
        "company_id": new_company_id,
        "name": "Operador",
        "description": "Lançar contas, mas não vê relatórios",
        "is_system_role": False
    }).execute()

    # 3. Vincula o Usuário logado como Dono da Empresa
    supabase_admin.table("user_company_links").insert({
        "user_id": user_id,
        "company_id": new_company_id,
        "role_id": owner_role_id,
        "is_active": True
    }).execute()

    return new_company_id