import logging
from typing import Any

from elasticsearch import Elasticsearch
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..transformations import to_frontend_results

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.DEBUG)

logger = logging.getLogger(__name__)


router = APIRouter()

templates: Jinja2Templates = Jinja2Templates(directory="templates")


def search_client() -> Elasticsearch:
    return Elasticsearch("http://localhost:9200")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, q: str = "") -> Any:
    es = search_client()
    if q:
        response = es.search_template(
            index="restaurants", body={"id": "all_text_fields", "params": {"query": q}}
        )
    else:
        response = es.search_template(index="restaurants", body={"id": "all_results"})

    logger.debug(f"Query: {q}")
    logger.debug(f"Response: {response}")

    results = to_frontend_results(response)
    logger.debug(f"Results: {results}")
    return templates.TemplateResponse(
        "index.html", {"request": request, "query": q, "results": results}
    )
