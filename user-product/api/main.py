from fastapi import FastAPI
from routes.routes import router_v1
from db.database import Base, engine

app = FastAPI()

# Create the database
Base.metadata.create_all(engine)

app.include_router(router_v1, prefix="/api/v1")
