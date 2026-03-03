# 1. Usamos a 3.14-slim para bater com a sua versão local
FROM python:3.14-slim

# Define a pasta de trabalho
WORKDIR /app

# Dependências do sistema (enxuguei para o essencial)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN pip install --no-cache-dir poetry

# --- O PULO DO GATO ---
# Copiamos o README.md junto com as dependências. 
# O '*' serve para não quebrar se o arquivo não existir por acaso.
COPY pyproject.toml poetry.lock* README.md* ./

# Configura o Poetry e instala as dependências
# Adicionamos o --no-cache para a imagem ficar mais leve
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main --no-root

# Copia o resto do código
COPY . .

# Expõe a porta 8000
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]