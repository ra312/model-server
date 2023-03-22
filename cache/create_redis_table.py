import csv
import json
import logging

import redis

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)


def csv_to_redis(
    filename: str,
    redis_host: str,
    redis_port: str,
    redis_db: str,
    hash_name: str,
    batch_size: int = 1000,
) -> None:
    # Connect to Redis
    logger.info("Connecting to Redis")
    r: redis.Redis[bytes] = redis.Redis(host=redis_host, port=int(redis_port), db=int(redis_db))

    # Read the CSV file and insert into Redis hash table
    with open(filename, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        pipe = r.pipeline()
        count = 0
        for row in reader:
            try:
                serialized_row = json.dumps(row)
                # use a unique key for each row, e.g., the row number
                pipe.hset(hash_name, f"row_{count}", serialized_row)
            except Exception as e:
                logger.error(f"Error inserting row {row}: {e}")
            else:
                count += 1
                if count % batch_size == 0:
                    try:
                        pipe.execute()
                    except Exception as e:
                        logger.error(f"Error executing pipeline: {e}")
        try:
            pipe.execute()
        except Exception as e:
            logger.error(f"Error executing pipeline: {e}")

    # Log completion message
    logger.info(
        f"CSV file {filename} successfully inserted into Redis hash table {hash_name} with {count} rows."
    )


csv_to_redis(
    filename="sessions.csv",
    redis_host="0.0.0.0",
    redis_port="6379",
    redis_db="0",
    hash_name="sessions",
)
