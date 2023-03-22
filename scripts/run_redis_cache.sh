set -eox pipefail

 echo "Redis CLI is not installed, installing..."
sudo apt-get update
sudo apt-get install -y redis-tools

echo "Building Docker image static-redis"
docker build -t static-redis .

echo "Starting Docker container"
docker run -ti --network host static-redis

echo "Loading compressed sessions data dump.rdb into Redis"
redis-cli --pipe dump.rdb
command -v redis-cli &> /dev/null
