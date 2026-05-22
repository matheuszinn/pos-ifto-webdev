# Use a imagem oficial do Python como base
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que o Flask usará
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=app:create_app()
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
