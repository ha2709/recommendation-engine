First Stop mySQL on your local

` systemctl stop mysql`

To run the app

`docker-compose up --build`

To run the app

`docker-compose up`

Run the app out side container:

`uvicorn main:app --reload`

If no data in DB, Run migration all dataset to Database :

```
docker exec -it user-product /bin/bash
python3 migration/migrate_all.py

```

To run Test

`pytest`

Sample request

```
curl -X 'GET' \
  'http://localhost:8001/api/v1/product' \
  -H 'accept: application/json' \
  -H 'access_token: supersecretkey'
```
