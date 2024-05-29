# MovieActorRanking
# Information Retrieval Evaluation

## documents

## requirements

* Python >=3.7
* Visual Studio Code

## Python

### unix/mac
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
```

### windows
```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
pip install --upgrade pip
```

## environment variables
* copy and rename the `.env.sample` file to `.env`

## database 
```bash
docker compose -f docker.compose.yml up -d
prisma db push
```

### optional: pgadmin
Open `http://localhost:5050/`
1) Email: root@root.com
2) Password: root

Click with the right mouse button on Servers and select Register -> Server.

Connection tab requires to type:
1) Host name/address: db
2) Port: 5432
3) Username: postgres
4) Password: postgres

## optional: swagger
Open `http://localhost:8000/docs` to see the swagger UI

## optional: Docker
building
```bash
docker build --tag tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/api:latest .
```

running container locally
```bash
docker run --detach --publish 3100:3100 tonylukeregistry.azurecr.io/tonylukeregistry/information-retrieval/api:latest
```


## optional: azure deployment
change connection string;
```bash
postgresql://<dbuser>:<dbpassword>@<dbservername>.postgres.database.azure.com:<port>/<bdname>?schema=public&sslmode=require
```



