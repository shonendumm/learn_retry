from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential, \
    stop_after_delay, wait_exponential_jitter, retry_if_not_exception_type, retry_if_exception_type
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)





@retry(stop=stop_after_attempt(5) | stop_after_delay(5), wait=wait_exponential_jitter(initial=2, min=2))
def do_something():
    logger.info("Doing something...")
    raise Exception("Something went wrong")



if __name__ == "__main__":
    do_something()