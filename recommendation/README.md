To build Docker image, run :

`docker build -t recommendation .`

To run Docker container

`docker run --network host recommendation`

On browser, navigate to `http://127.0.0.1:8000/docs`

```
curl -X 'GET' \
  'http://localhost:8000/api/v1/recommend/103' \
  -H 'accept: application/json' \
  -H 'access_token: supersecretkey'
```

For local development:

`uvicorn main:app --reload --port 8000`

To run the tests: 

`pytest`
