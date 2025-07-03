import signal
import sys
import logging
from app.scheduler import run_loop

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def shutdown(signum, frame):
    logging.info("Shutting down gracefully...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    logging.info("Govee controller starting...")
    run_loop()
