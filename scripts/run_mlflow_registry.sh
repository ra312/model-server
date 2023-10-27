#!/bin/bash
set -o pipefail
set -euox

docker run -p 5000:5000 mlflow-arm64:2.2.2
