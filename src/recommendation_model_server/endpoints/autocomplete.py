from elasticsearch import Elasticsearch
from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse

from ..transformations import to_frontend_suggestions

router = APIRouter()


def get_local_client() -> Elasticsearch:
    return Elasticsearch("http://localhost:9200")


@router.get("/autocomplete")
async def autocomplete(request: Request, q: str = Query("")) -> JSONResponse:
    es = get_local_client()
    response = es.search(
        index="restaurants",
        body={
            "suggest": {
                "autocomplete": {
                    "prefix": q,
                    "completion": {
                        "field": "suggest",
                        "skip_duplicates": True,
                    },
                }
            },
            "_source": "title",
        },
    )

    return JSONResponse(to_frontend_suggestions(response))
