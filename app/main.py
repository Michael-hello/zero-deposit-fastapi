from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.database import init_db
from app.api.property.routes import router as properties_router


# Initialize database on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown
    pass


app = FastAPI(lifespan=lifespan)

app.include_router(properties_router)


@app.get("/")
async def root():
    return {"message": "Zero Deposit: Property Management"}


