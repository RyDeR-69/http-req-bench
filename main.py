import aiohttp
import requests
import httpx
import asyncio
from loguru import logger
from time import perf_counter

url = 'https://example.com/'


def req(count: int):
    start = perf_counter()
    for _ in range(count):
        requests.get(url)
    logger.debug(f"requests executed in {perf_counter() - start}")


def session_req(count: int):
    start = perf_counter()
    session = requests.session()
    for _ in range(count):
        session.get(url)
    logger.debug(f"session  requests executed in {perf_counter() - start}")


def sync_httpx(count: int):
    start = perf_counter()
    with httpx.Client() as client:
        for _ in range(count):
            client.get(url)
    logger.debug(f"sync httpx executed in {perf_counter() - start}")


async def async_httpx():
    async with httpx.AsyncClient() as client:
        await client.get(url)


async def aio():
    async with aiohttp.ClientSession() as client:
        await client.get(url)


async def main(count: int):
    req(count)
    session_req(count)
    sync_httpx(count)

    start = perf_counter()
    await asyncio.gather(*[asyncio.create_task(async_httpx()) for _ in range(count)])
    logger.debug(f"async httpx executed in {perf_counter() - start}")

    start = perf_counter()
    await asyncio.gather(*[asyncio.create_task(aio()) for _ in range(count)])
    logger.debug(f"aiohttp httpx executed in {perf_counter() - start}")


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(10))
