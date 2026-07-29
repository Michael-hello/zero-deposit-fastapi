from fastapi import FastAPI

from app.db.database import init_db
from app.api.property.routes import router as properties_router
from app.logging import setup_logging



#setup db and logging
init_db()
setup_logging()

app = FastAPI(title="test-app")

#register routes
app.include_router(properties_router)




