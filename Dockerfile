# Utilizamos uma imagem oficial do Python na versão 3.10 (Slim) 
# para garantir um ambiente leve e focado apenas na execução do projeto [cite: 43]
FROM python:3.10-slim

# Definimos o diretório de trabalho dentro do container onde o código será armazenado
WORKDIR /app

# Instalamos dependências do sistema necessárias para compilação de algumas bibliotecas de ML, se houver
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos primeiro apenas o arquivo de requisitos para aproveitar o cache do Docker
# Isso agiliza a criação da imagem caso o código mude, mas as bibliotecas continuem as mesmas
COPY requirements.txt .

# Realizamos a instalação de todas as bibliotecas listadas (Pandas, Scikit-Learn, FastAPI, etc.) [cite: 44, 45, 60]
RUN pip install --no-cache-dir -r requirements.txt

# Agora copiamos todo o restante do código do projeto para dentro do container [cite: 78]
COPY . .

# Expomos a porta 8000, que é a porta padrão onde a nossa API FastAPI irá rodar [cite: 27]
EXPOSE 8000

# Definimos o comando principal para iniciar a nossa aplicação.
# O Uvicorn servirá a API principal, permitindo conexões externas através do host 0.0.0.0 
CMD ["uvicorn", "app.api_principal:aplicativo_api", "--host", "0.0.0.0", "--port", "8000"]