from fastapi import FastAPI
import auth_router
from products_router import router
from database import engine, Base
from models import Book
from fastapi_jwt_auth2 import AuthJWT
from schemas import Settings

@AuthJWT.load_config
def get_config():
    return Settings()


app = FastAPI()



Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="/books")
app.include_router(auth_router.auth_router, prefix="/auth")