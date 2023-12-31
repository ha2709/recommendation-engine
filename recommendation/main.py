from fastapi import FastAPI
from routes import router_v1

app = FastAPI()
app.include_router(router_v1, prefix="/api/v1")
