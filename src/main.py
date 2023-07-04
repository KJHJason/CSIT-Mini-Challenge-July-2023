from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.responses import ORJSONResponse
from api import api_router
import orjson

class PrettyORJSON(ORJSONResponse):
    """A modified version of the ORJSONResponse 
    class that returns an indented JSON response.
    """
    def render(self, content: dict[str, str]) -> bytes:
        return orjson.dumps(
            content, 
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2,
        )

app = FastAPI(
    title="CSIT Mini Challenge July 2023 by KJHJason",
    debug=True,
    version="1.0.0",
    default_response_class=PrettyORJSON,
    swagger_ui_oauth2_redirect_url=None,
)
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "CSIT Mini Challenge July 2023",
        "author": "KJHJason",
        "Routes": [
            "/flight",
            "/hotel",
            "/docs",
            "/redoc",
        ],
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="localhost", 
        port=8080,
        reload=True,
        log_level="debug",
    )
