from fastapi import FastAPI

from app.db.database import init_db
from app.api.property.routes import router as properties_router



#setup db
init_db()


app = FastAPI(title="test-app")

#register routes
app.include_router(properties_router)




