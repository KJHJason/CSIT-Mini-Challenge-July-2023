from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError
from api import (
    api_router,
    PrettyORJSON,
)

DESC = """CSIT Mini Challenge July 2023 by KJHJason

GitHub: https://github.com/KJHJason

This API is built with Python 3.11 using FastAPI as its framework.
"""
INDEX_RESPONSE = {
    "message": "CSIT Mini Challenge July 2023",
    "author": "KJHJason",
    "github": "https://github.com/KJHJason",
    "api_routes": [
        "/flight",
        "/hotel",
    ],
    "documentation_routes": [
        "/docs",
        "/redoc",
    ],
}

app = FastAPI(
    title="CSIT Mini Challenge",
    description=DESC,
    debug=True,
    version="1.0.0",
    default_response_class=PrettyORJSON,
    swagger_ui_oauth2_redirect_url=None,
)
app.include_router(api_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=400)

@app.get("/")
def index():
    return INDEX_RESPONSE

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8080,
        reload=True,
    )
