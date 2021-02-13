from aiohttp import web
from aiohttp import WSMsgType
from aiohttp import ClientSession

from json import loads, dumps
from re import compile, match

from asyncio import wait, get_event_loop
from bs4 import BeautifulSoup as bs

import aiohttp_jinja2
import jinja2

from logging import getLogger

app = web.Application()
routes = web.RouteTableDef()
logger = getLogger("app")
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader("templates"))


@routes.view('/ws')
class WebSocket(web.View):
    USERS = set()

    @staticmethod
    def event_state(url, uniqueId):
        return dumps({"type": "state", "url": url, "id": uniqueId})

    @staticmethod
    def update_state(uniqueId, state):
        return dumps({"type": "update", "id": uniqueId, "state": state})

    @staticmethod
    async def notify_user(data, uniqueId):
        if WebSocket.USERS:
            message = WebSocket.event_state(data, uniqueId)
            logger.info(f"Message: {message}")
            await wait([user.send_str(message) for user in WebSocket.USERS])

    @staticmethod
    async def notify_update(uniqueId, state):
        if WebSocket.USERS:
            message = WebSocket.update_state(uniqueId, state)
            await wait([user.send_str(message) for user in WebSocket.USERS])

    @staticmethod
    async def crawl(websocket, uniqueId, url, pages=None):
        rePattern = compile(r'^https?:/{2,}\S+')

        async with ClientSession() as session:
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
            if match(rePattern, links['href']):
                if pages is not None:
                    for link in pages:
                        if link in soup:
                            soup.remove(link)
                if len(soup) == 0:
                    return
                await WebSocket.notify_update(uniqueId, links['href'])
                try:
                    await WebSocket.crawl(websocket, uniqueId, links['href'], pages=soup)
                except UnicodeDecodeError:
                    pass

    async def get(self):
        try:
            uniqueId    = 0
            websocket   = web.WebSocketResponse()
            coro        = get_event_loop()
            await       websocket.prepare(self.request)
        except Exception:
            return
        try:
            WebSocket.USERS.add(websocket)
            async for message in websocket:
                if message.type == WSMsgType.TEXT:
                    data = loads(message.data)
                    if data is not None:
                        if match(r'^https?://.*', data['url']):
                            await self.notify_user(data['url'], uniqueId)
                            coro.create_task(WebSocket.crawl(websocket, uniqueId, data['url']))
                            uniqueId += 1
        finally:
            WebSocket.USERS.remove(websocket)

        return websocket


@routes.view('/')
class UserView(web.View):

    @aiohttp_jinja2.template('index.html')
    async def get(self):
        return

    async def post(self):
        pass


if __name__ == '__main__':
    app.router.add_routes(routes)
    app.router.add_static('/static', 'static', name='static')
    web.run_app(app)