from fastapi import FastAPI, Request
from elasticsearch import Elasticsearch
import logging
import uuid
import json

app = FastAPI()
logger = logging.getLogger("log_collector")
logging.basicConfig(level=logging.INFO)

# Connect to ES with explicit API version
es = Elasticsearch(
    "http://elasticsearch:9200",
    headers={"Accept": "application/vnd.elasticsearch+json; compatible-with=7",
             "Content-Type": "application/vnd.elasticsearch+json; compatible-with=7"}
)

@app.post("/collect")
async def collect_logs(request: Request):
    data = await request.body()
    log_line = data.decode("utf-8")
    logger.info(f"Received: {log_line}")
    
    # Send to ES
    try:
        es.index(index="logs", id=str(uuid.uuid4()), document={"message": log_line})
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Failed to index log: {str(e)}")
        return {"status": "error", "message": str(e)}, 500
