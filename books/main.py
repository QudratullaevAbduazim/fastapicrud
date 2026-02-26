from fastapi import FastAPI
import auth_router
from products_router import router
from database import engine, Base
from models import Book



app = FastAPI()



Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/books")
app.include_router(auth_router.auth_router, prefix="/auth")