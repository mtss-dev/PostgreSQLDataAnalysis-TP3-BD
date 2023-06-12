# TP3 - Banco de Dados 1

## Alunos

- Matheus Dos Santos Palheta -22052572

- Matheus Silva dos Santos - 22052573

- Vinícius Luiz Nunes da Fonseca - 22050031

## Objetivo

- Este trabalho tem como objetivo responder as questões propostas no Trabalho Prático 3 da disciplina de Banco de Dados 1, cujo documento está disponível [aqui](https://docs.google.com/document/d/17Uobq1brb6TbbCr64DWCEWG9J-LAGpgXuOC3BVpczx4/edit#heading=h.gjdgxs).  Foram utilizados códigos escritos em Python e SQL, e os dados foram armazenados em um banco de dados PostgreSQL. O trabalho foi realizado em um container Docker, e os dados foram persistidos em um volume para evitar perdas ao reiniciar o container. Além disso, as partes relacionadas à codificação foram executadas em scripts .py, separados do notebook principal, a fim de manter a organização e evitar poluição visual. O notebook foi utilizado para visualização dos dados e para responder às questões de análise propostas.

## Como executar

Criar a imagem
```bash
docker build -t tp3 .
```

Criar o container
```bash
docker run -d --shm-size=1g --name tp3 -p 5433:5432 -p 8888:8888 -v $(pwd)/notebooks/:/app/notebooks -v $(pwd)/datadir/:/app/datadir tp3
```

Iniciar o jupyter notebook dentro do container
```bash
docker exec tp3 jupyter notebook --notebook-dir=/app/notebooks/ --allow-root --ip 0.0.0.0 --no-browser
```

Cria a imagem, cria o container e inicia o jupyter notebook
```bash
docker build -t tp3 . && docker run -d --shm-size=1g --name tp3 -p 5433:5432 -p 8888:8888 -v $(pwd)/notebooks/:/app/notebooks -v $(pwd)/datadir/:/app/datadir tp3 && docker exec tp3 jupyter notebook --notebook-dir=/app/notebooks/ --allow-root --ip 0.0.0.0 --no-browser
```

## Outros comandos úteis

Iniciar o container
```bash
docker start tp3
```

Parar o container
```bash
docker stop tp3
```

Remover todos os containers
```bash
docker rm -f $(docker ps -aq)
```

Remover todas as imagens
```bash
docker rmi -f $(docker images -aq)
```

Excluir a imagem e o container
```bash
docker container rm tp3 && docker image rm tp3
```

Iniciar o jupyter notebook dentro do container
```bash
docker exec tp3 jupyter notebook --notebook-dir=/app/notebooks/ --allow-root --ip 0.0.0.0 --no-browser
```

Entrar no postgresql dentro do container
```bash
docker exec -it tp3 psql -h localhost -p 5432 -U postgres -W
```
