from tenacity import retry, stop_after_attempt, wait_fixed, wait_exponential, \
    stop_after_delay, wait_exponential_jitter, retry_if_not_exception_type, retry_if_exception_type, retry_if_result, TryAgain
import logging
import random
import typer

app = typer.Typer()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class CustomException(Exception):
    pass

@app.command()
@retry(retry=retry_if_not_exception_type(CustomException), stop=stop_after_attempt(50) | stop_after_delay(20), wait=wait_exponential_jitter(initial=2))
def do_something_repeatedly():
    logger.info("Rolling dice...")
    randint = random.randint(0, 10)
    logger.info(f"Random number: {randint}")
    if randint < 1: # 0
        logger.info("Success")
        print("Success")
        return True
    elif randint == 1: 
        raise CustomException("Stop now.")
    else: 
        logger.info("Try again")
        raise Exception("Try again")



def is_none(result):
    return result == None
    
# keep retrying for all exceptions and if result is None
@app.command()
@retry(retry=retry_if_exception_type() | retry_if_result(is_none), stop=stop_after_attempt(50) | stop_after_delay(20))
def retry_for_all_exceptions_or_none():
    logger.info("Rolling dice...")
    randint = random.randint(0, 10)
    logger.info(f"Random number: {randint}")
    if randint < 1: # 0
        logger.info("Success")
        print("Success")
        return True
    elif randint <= 3: 
        raise CustomException("Stop now.")
    else: 
        logger.info("Try again")
        return None

# keep retrying if result is None and explicitly raise TryAgain
@app.command()
@retry(retry=retry_if_result(is_none), stop=stop_after_attempt(10) | stop_after_delay(20))
def retry_if_result_none():
    logger.info("retry_if_result_none...")
    randint = random.randint(0, 10)
    logger.info(f"Random number: {randint}")
    if randint < 1: # 0
        logger.info("Success")
        print("Success")
        return True
    elif randint <= 5: 
        logger.info("Answer is not None")
        return 10
    else:
        return None
    
# Add exception handling to return None
# But at the end of all retries, returning None will cause a RetryError. So the function still must be in a try/except block.
@app.command()
@retry(retry=retry_if_exception_type() | retry_if_result(is_none), stop=stop_after_attempt(3) | stop_after_delay(20))
def retry_if_result_exception():
    randint = random.randint(0, 10)
    logger.info(f"Random number: {randint}")
    if randint < 1: # 0
        logger.info("Success")
        print("Success")
        return 0
    elif randint < 3: 
        # logger.info("Breaking the loop")
        # break # will cause break error
        logger.info(f"{randint=}")
        return None
    else:
        raise Exception("I summon Exception")


    
@app.command()
def wrap_func():
    try:
        logger.info("Calling wrap_func")
        res = retry_if_result_exception()
        return res
    except Exception as e:
        logger.info(str(e))
        return None



if __name__ == "__main__":

    # do_retry_explictly()
    # retry_for_all_exceptions_or_none()
    # retry_if_result_none()
    # res = retry_if_result_none_exception()
    res = wrap_func()
    print("result is", res)
