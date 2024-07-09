from fastapi import FastAPI, Header, Body, Query, Path, Request
from enum import Enum
from typing import Optional, Annotated
from fastapi.responses import RedirectResponse, Response
from products_routes import product_router
from orders_routes import orders_router
from auth_routes import auth_router
from fastapi.responses import RedirectResponse, Response, JSONResponse
from fastapi_jwt_auth import AuthJWT
from schemas_auth import Settings

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()



app.include_router(product_router)
app.include_router(orders_router)
app.include_router(auth_router)



