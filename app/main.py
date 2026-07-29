from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.logging import setup_logging
from app.db.database import init_db

from app.api.property.routes import router as properties_router
from app.api.auth.routes import router as auth_router



#setup db and logging
init_db()
setup_logging()

app = FastAPI(title="test-app")

#register routes
app.include_router(properties_router)
app.include_router(auth_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],  # Change to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



