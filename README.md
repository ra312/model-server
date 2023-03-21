# inference service
```mermaid
flowchart TD
    A[ModelArtifact] -->B(Model Instance)
    E[Restaurants_Index:Elastic] -->B
    F[Restaurant API] -->B
    %% G[InferenceFeatures: ES_Index] -->B
    %% G --> H
    B -->C[VenueRatings] --> H(Elastic)
    %% H[ElasticIndex] --> B
    C -- 100 rps with 2s response single cpu-->D(Search List)

```

[![PyPI](https://img.shields.io/pypi/v/recommendation-model-server?style=flat-square)](https://pypi.org/project/recommendation-model-server/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/model-server?style=flat-square)](https://pypi.org/project/recommendation-model-server/)
[![PyPI - License](https://img.shields.io/pypi/l/model-server?style=flat-square)](https://pypi.org/project/recommendation-model-server/)
[![Coookiecutter - Wolt](https://img.shields.io/badge/cookiecutter-Wolt-00c2e8?style=flat-square&logo=cookiecutter&logoColor=D4AA00&link=https://github.com/woltapp/wolt-python-package-cookiecutter)](https://github.com/woltapp/wolt-python-package-cookiecutter)
[![codecov](https://codecov.io/gh/ra312/personalization/branch/main/graph/badge.svg?token=2K6174OLAI)](https://codecov.io/gh/ra312/personalization)

---

**Training Pipeline Source Code**: [https://github.com/ra312/personalization](https://github.com/ra312/personalization)
**Source Code**: [https://github.com/ra312/model-server](https://github.com/ra312/model-server)

---

A service to rate venues

## Installation

```sh
python3 -m pip install recommendation-model-server
```

## Running locally on host
If you choose to use pre-trained model in artifacts/rate_venues.pickle to start on 0.0.0.0:8000
```sh
/scripts/start_inference_service.sh
```
In separate tab, please run
```sh
curl -X 'POST' \
'http://0.0.0.0:8000/predict' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '[
  {
    "venue_id": -4202398962129790000,
    "conversions_per_impression": 0.3556765815,
    "price_range": 1,
    "rating": 8.6,
    "popularity": 4.4884057024,
    "retention_rate": 8.6,
    "session_id_hashed": 3352618370338455600,
    "position_in_list": 31,
    "is_from_order_again": 0,
    "is_recommended": 0
  }
]'
```
## Running in container
```sh
docker pull akylzhanov/search-api
docker run -d --name search-api-container -p 8000:8000 --rm akylzhanov/search-api
```
# Start search UI
## Start elasticindex locally
```sh
./scripts/run_elastic_locally.sh
```
## Create restaurant index querying local restaurants for lat=52.5024674, lon = 13.2810506 at Café Am Neuen See, Tiergarten, Mitte
```sh
poetry run python3 src/recommendation_model_server/indexer.py
```
## Head to search UI at localhost:8000
![alt text](search_ui.png)

## Development

* Clone this repository
* Requirements:
  * [Poetry](https://python-poetry.org/)
  * Python 3.10.10
* Create a virtual environment and install the dependencies

```sh
poetry install
```

* Activate the virtual environment

```sh
poetry shell
```

### Testing

```sh
pytest tests
```


### Pre-commit

Pre-commit hooks run all the auto-formatters (e.g. `black`, `isort`), linters (e.g. `mypy`, `flake8`), and other quality
 checks to make sure the changeset is in good shape before a commit/push happens.

You can install the hooks with (runs for each commit):

```sh
pre-commit install
```

Or if you want them to run only for each push:

```sh
pre-commit install -t pre-push
```

Or if you want e.g. want to run all checks manually for all files:

```sh
pre-commit run --all-files
```

---

### How to run load tests
1. Start service locally, host=0.0.0.0, port=8000
```sh
/scripts/start_inference_service.sh
```
 2. Run load test with locust 1million users with spawn rate 100 users per second, i.e.
 ```sh
 poetry shell && pytest tests/test_invokust_load.py -s
 ```
 The output is similar to (the time is in milliseconds)
 ```sh
 Ramping to 1000000 users at a rate of 100.00 per second
Type     Name  # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------||-------|-------------|-------|-------|-------|-------|--------|-----------
POST     /predict    1453     0(0.00%) |    448       5    1948    390 |  167.83        0.00
--------||-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated    1453     0(0.00%) |    448       5    1948    390 |  167.83        0.00
  ```
This project was generated using the [wolt-python-package-cookiecutter](https://github.com/woltapp/wolt-python-package-cookiecutter) template.
