import asyncio
import ipaddress
import os
from pathlib import Path

from aiohttp import ClientSession, ClientTimeout, WSMsgType, web

HOST = os.environ.get("HA_URL", "").rstrip("/")
TOKEN = os.environ.get("HA_ACCESS_TOKEN", "")
DISPLAY_NETWORKS = [
    ipaddress.ip_network(value.strip(), strict=False)
    for value in os.environ.get("HUB_DISPLAY_IPS", "").split(",")
    if value.strip()
]
HTML = Path(__file__).with_name("hub.html")

def authorize(request):
    if not request.remote or not any(
        ipaddress.ip_address(request.remote) in network for network in DISPLAY_NETWORKS
    ):
        raise web.HTTPForbidden(text="This display is not allowed.")
    if not HOST or not TOKEN:
        raise web.HTTPServiceUnavailable(text="Configure the Home Assistant connection in Arcane.")

async def index(request):
    authorize(request)
    return web.FileResponse(HTML, headers={"Cache-Control": "no-store"})

async def socket(request):
    authorize(request)
    origin = request.headers.get("Origin")
    if origin != f"{request.scheme}://{request.host}":
        raise web.HTTPForbidden()
    async with ClientSession(timeout=ClientTimeout(total=None, connect=10)) as session:
        async with session.ws_connect(HOST + "/api/websocket", heartbeat=30, max_msg_size=32 * 1024 * 1024) as upstream:
            if (await upstream.receive_json(timeout=10)).get("type") != "auth_required":
                raise web.HTTPBadGateway()
            await upstream.send_json({"type": "auth", "access_token": TOKEN})
            if (await upstream.receive_json(timeout=10)).get("type") != "auth_ok":
                raise web.HTTPBadGateway(text="Home Assistant rejected the configured credential.")
            browser = web.WebSocketResponse(heartbeat=30)
            await browser.prepare(request)
            await browser.send_json({"type": "auth_ok", "ha_url": HOST})

            async def relay(source, destination):
                async for message in source:
                    if message.type == WSMsgType.TEXT:
                        await destination.send_str(message.data)

            tasks = [
                asyncio.create_task(relay(browser, upstream)),
                asyncio.create_task(relay(upstream, browser)),
            ]
            try:
                await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            finally:
                for task in tasks:
                    task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
                await browser.close()
            return browser

async def health(request):
    return web.Response(text="ok")

app = web.Application()
app.add_routes([web.get("/", index), web.get("/api/websocket", socket), web.get("/health", health)])
web.run_app(app, port=80)
