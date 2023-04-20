from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exception: AuthJWTException):
    return JSONResponse(status_code=exception.status_code, content={"detail": exception.message})


@app.get("/get_headers_access")
def get_headers_access(authorize: AuthJWT = Depends()):
    authorize.jwt_required()
    return authorize.get_unverified_jwt_headers()


@app.get("/get_headers_refresh")
def get_headers_refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()
    return authorize.get_unverified_jwt_headers()
