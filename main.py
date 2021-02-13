import asyncio
import time

import aiohttp

import websockets
import json
import re

from bs4 import BeautifulSoup as bs
from functools import partial

USERS = set()


def event_state(url, uniqueId):
    return json.dumps({"type": "state", "url": url, "id": uniqueId})


def update_state(uniqueId, state):
    return json.dumps({"type": "update", "id": uniqueId, "state": state})


async def notify_user(url, uniqueId):
    if USERS:
        message = event_state(url, uniqueId)
        print(message)
        await asyncio.wait([user.send(message) for user in USERS])


async def notify_update(uniqueId, state):
    if USERS:
        message = update_state(uniqueId, state)
        await asyncio.wait([user.send(message) for user in USERS])


async def crawl(websocket, uniqueId, url, pages=None):
    rePattern = re.compile(r'^https?:/{2,}\S+')

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                assert resp.status == 200
                parsedData = await resp.text()
            except AssertionError:
                parsedData = ""
                pass

    soup = bs(str(parsedData), "lxml").find_all("link")

    if len(soup) == 0:
        return

    for links in soup:
        if re.match(rePattern, links['href']):
            if pages is not None:
                for link in pages:
                    if link in soup:
                        soup.remove(link)
                print(soup)
            if len(soup) == 0:
                return
            await notify_update(uniqueId, links['href'])
            try:
                await crawl(websocket, uniqueId, links['href'], pages=soup)
            except UnicodeDecodeError:
                pass


async def server(websocket, path):
    USERS.add(websocket)
    coro = asyncio.get_event_loop()

    try:
        uniqueId = 0
        async for message in websocket:
            data = json.loads(message)
            if data['url'] is not None:
                if re.match(r'^https?:\/\/.*', data['url']):
                    await notify_user(data['url'], uniqueId)
                    coro.create_task(crawl(websocket, uniqueId, data['url']))
                    uniqueId += 1
            else:
                print("Unsupported event")
                await websocket.send(json.dumps({"type": "error", "error": "Unsupported event"}))
    finally:
        USERS.remove(websocket)


if __name__ == '__main__':
    start_server = websockets.serve(server, host='localhost', port=9090)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    print("Server started")
    loop.run_forever()
