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

    # 2. Ativa Módulos Padrão
    modules = supabase_admin.table("app_modules").select("id, slug").in_("slug", ["finance", "settings"]).execute()
    
    if modules.data:
        modules_insert = [{"company_id": new_company_id, "module_id": m['id']} for m in modules.data]
        supabase_admin.table("company_modules").insert(modules_insert).execute()

    # 3. Configura a Régua de Cobrança
    supabase_admin.table("company_settings").insert({
        "company_id": new_company_id,
        "financial_delay_tolerance_days": 5,
        "financial_delay_critical_days": 15
    }).execute()

    # 4. Cria Cargos Base
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

    # 5. Vincula o Usuário logado como Dono da Empresa
    supabase_admin.table("user_company_links").insert({
        "user_id": user_id,
        "company_id": new_company_id,
        "role_id": owner_role_id,
        "is_active": True
    }).execute()

# 6. Cria o Plano de Contas Padrão
    default_cats = [
        {"name": "Receita Operacional", "type": "income", "is_editable": False, "company_id": new_company_id},
        {"name": "Impostos sobre Venda", "type": "expense", "is_editable": False, "company_id": new_company_id},
        {"name": "Custos Variáveis (CMV)", "type": "expense", "is_editable": False, "company_id": new_company_id},
        {"name": "Despesas Fixas", "type": "expense", "is_editable": False, "company_id": new_company_id},
        {"name": "Pró-Labore / Lucros", "type": "expense", "is_editable": True, "is_dre_visible": False, "company_id": new_company_id}
    ]
    
    supabase_admin.schema("finance").table("categories").insert(default_cats).execute()

    return new_company_id