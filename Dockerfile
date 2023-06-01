# Utilizaremos a imagem do ubuntu
FROM ubuntu:latest

# Definir a variável de ambiente DEBIAN_FRONTEND para evitar interações interativas
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Instalação do python3, python3-pip, libpq-dev, wget e lsb-release
RUN apt update && apt install -y python3 python3-pip libpq-dev wget lsb-release

# Instalação do postgresql diretamente do site oficial
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list' && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt update && \
    apt install -y postgresql

# Criação do usuário postgres e definição da senha, e criação do banco de dados "tpch"
RUN service postgresql start && \
    su - postgres -c "psql -c \"ALTER USER postgres WITH PASSWORD 'postgres';\"" && \
    su - postgres -c "createdb tpch" && \
    su - postgres -c "createdb series" && \
    service postgresql stop

# Definir o diretório de trabalho
WORKDIR /app
COPY . /app

# Instalação das dependências do projeto
RUN pip install -r requirements.txt

# Definir o CMD para iniciar o PostgreSQL
CMD service postgresql start && tail -f /dev/null