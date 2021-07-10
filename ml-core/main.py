import requests
from fastapi import FastAPI
from fastapi.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute

from error_handlers.warnings import WarningJSON
from error_handlers.exceptions import ExceptionJSON
from training.training import train_models
from database.users.connection import Base, engine, create_session
from models.User import User
from serializers import UserSerializer

DEFAULT_WARNING_CODE = 209
DEFAULT_ERROR_CODE = 500

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.exception_handler(WarningJSON)
async def warning_json_handler(request, exc):
    return JSONResponse(
        content={"warning": {"detail": exc.detail}},
        status_code=DEFAULT_WARNING_CODE,
    )


@app.exception_handler(ExceptionJSON)
async def exception_json_handler(request, exc):
    return JSONResponse(
        content={"exception": {"detail": exc.detail}},
        status_code=DEFAULT_ERROR_CODE,
    )


@app.middleware("http")
async def jwt_authentication(request: Request, call_next):
    """JWT authentication middleware.

    :param request: Current request.
    :param call_next: Next middleware.
    :return: Response.
    """

    def __check_route_include_schema(routes: BaseRoute, request: Request) -> bool:
        """Check whether the route included to the route scheme.

        :param routes: All routes.
        :param request: Current request.
        :return: Included schema or not.
        """
        for route in routes:
            if route.path == request.url.path and route.include_in_schema:
                return True
        return False

    if __check_route_include_schema(app.routes, request):
        token = request.headers.get("authorization")
        if not token:
            return JSONResponse(
                status_code=401,
                content={"exception": {"detail": "Token doesn't exist."}},
            )

        request_verifying = requests.get(
            "http://auth:8080/verify_token/", params={"token": token}
        )

        if request_verifying.status_code != 200:
            return JSONResponse(
                status_code=request_verifying.status_code,
                content={"exception": {"detail": request_verifying.json()}},
            )
        else:
            response = request_verifying.json()
            with create_session() as db:
                user = db.query(User).get(response.get("id"))

            user = UserSerializer.from_orm(user)
            user.token = token
            request.scope["user"] = user
    response = await call_next(request)

    return response


@app.post("/train/")
async def train(request: Request):
    return train_models(request.scope["user"])
