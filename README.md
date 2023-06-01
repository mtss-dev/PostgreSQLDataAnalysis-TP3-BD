# tp3-bd

## Comandos essenciais para o uso do docker

Remover todos os containers
```bash
docker rm -f $(docker ps -aq)
```

Remover todas as imagens
```bash
docker rmi -f $(docker images -aq)
```

Limpar o cache (opcional)
```bash
docker builder prune -f
```

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

Entrar no postgresql dentro do container
```bash
docker exec -it tp3 psql -h localhost -p 5432 -U postgres -W
```

Excluir a imagem e o container
```bash
docker container rm tp3 && docker image rm tp3
```

Iniciar o container 
```bash
docker start tp3
```

Parar o container
```bash
docker stop tp3
```

Comando para testes (faz o uso de várias linhas de comando)
```bash
docker container rm tp3 && docker image rm tp3 && docker build -t tp3 . && docker run -d --shm-size=1g --name tp3 -p 5433:5432 -p 8888:8888 -v $(pwd)/notebooks/:/app/notebooks -v $(pwd)/datadir/:/app/datadir tp3
```
