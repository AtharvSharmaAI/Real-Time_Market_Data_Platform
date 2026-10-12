# OWNER: SHARED
#
# PURPOSE:
# Single-process "core" app used for Unikraft Cloud (and handy locally).
# Runs generator -> processor pipeline -> storage in a background thread, and
# serves the FastAPI app under /api plus the built frontend under /.
#
# Storage is SQLite unless CLICKHOUSE_HOST is set; Kafka is used only if
# confluent-kafka is installed and KAFKA_BOOTSTRAP_SERVERS points at a broker.
#
# Run: uvicorn main:app --port 8080

import logging
import os
import threading
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.app import database
from api.app.main import app as api_app
from generator.src.config import settings as gen_settings
from generator.src.generator import MarketDataGenerator
from processor.src.main import ProcessingPipeline

logger = logging.getLogger("core")
FRONTEND_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend", "dist")


class GeneratorSource:
    """Stands in for KafkaTradeConsumer: feeds generated events straight into the pipeline."""

    def __init__(self):
        self.gen = MarketDataGenerator()
        self.delay = 1.0 / max(gen_settings.event_rate, 1)

    def poll_messages(self, limit: int = 1000):
        for event in self.gen.generate_events(limit=limit):
            yield event
            time.sleep(self.delay)

    def commit(self):
        pass


def run_pipeline():
    sinks = {}
    if database.USE_SQLITE:
        sinks = {"on_trade": database.insert_raw, "on_window": database.insert_window}
    ProcessingPipeline(consumer=GeneratorSource(), **sinks).run(limit=10**12)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    threading.Thread(target=run_pipeline, name="pipeline", daemon=True).start()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/api", api_app)
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
