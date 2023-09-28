import json
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from app.core import http_client
from app.factory import create_app

app = create_app()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if type(exc.detail) is str:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
    if (
        exc.detail.get("error_description") is not None
        or exc.detail.get("error_codes") is not None
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail.get("error_description"),
                "error_codes": exc.detail.get("error_codes"),
            },
        )
    if exc.detail.get("error") is not None:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail.get("error").get("message"),
                "error_codes": exc.detail.get("error").get("code"),
            },
        )
    if exc.detail.get("detail").get("error") is not None:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail.get("detail").get("error").get("message"),
                "error_codes": [exc.detail.get("detail").get("error").get("code")],
            },
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail.get("detail")},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    exc_json = json.loads(exc.json())
    response = {"detail": ""}
    error = exc_json[0]
    response["detail"] = error["loc"][-1] + f" {error['msg']}"

    return JSONResponse(response, status_code=422)


@app.on_event("startup")
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """


@app.on_event("shutdown")
async def shutdown_event():
    await http_client.close()


@app.get("/", tags=["Heath Check"], status_code=status.HTTP_200_OK)
async def health_check():
    return "Service runs well"


@app.get("/api/v1/version", tags=["Heath Check"], status_code=status.HTTP_200_OK)
async def get_version():
    return "v0.1 2023/08/24"
