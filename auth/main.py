from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response

from authentication.token import decode_jwt
from authentication.sign_in import auth_user
from authentication.register import create_user

from database import engine, Base

from serializers import (
    UserSerializer,
    UserCredentialsSerializer,
    AuthResponseSerializer,
    VerifyTokenResponse,
)


TABLES_TO_CREATE = (
    Base.metadata.tables["users"],
    Base.metadata.tables["user_settings"],
    Base.metadata.tables["user_filter"],
    Base.metadata.tables["user_qa_metrics_filter"],
    Base.metadata.tables["user_predictions_table"],
)

Base.metadata.create_all(bind=engine, tables=TABLES_TO_CREATE)

app = FastAPI()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        content={"exception": {"detail": exc.detail}}, status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exception_detail = [
        {"name": error.get("loc")[1], "errors": [error.get("msg")]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=400, content=jsonable_encoder({"exception": exception_detail}),
    )


@app.post("/sign_in/", response_model=AuthResponseSerializer)
def sign_in(user: UserCredentialsSerializer):
    user = auth_user(user)
    return JSONResponse(user)


@app.post("/register/")
async def register(user: UserSerializer):
    await create_user(user)
    return Response(status_code=200)


@app.get("/verify_token/", response_model=VerifyTokenResponse)
def verify_token(token: str):
    response = {"id": decode_jwt(token)}
    return JSONResponse(response)
