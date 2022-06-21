import grequests
from loguru import logger
from time import perf_counter

url = "https://example.com"


def greq(count: int):
    start = perf_counter()
    rs = (grequests.get(url) for _ in range(count))
    grequests.map(rs)
    logger.debug(f"grequests executed in {perf_counter() - start} seconds...")


greq(100)
