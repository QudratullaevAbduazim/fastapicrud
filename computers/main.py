from fastapi import FastAPI
from products import router
from database import engine, Base
from models import Computer



app = FastAPI()



Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/computers")