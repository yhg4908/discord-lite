import asyncio
import websockets
import json

class Gateway:
    """Handles WebSocket connection to Discord Gateway"""
    GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, token, intents, event_handlers):
        self.token = token
        self.intents = intents
        self.event_handlers = event_handlers
        self.connection = None

    async def connect(self):
        """Connects to the Discord Gateway"""
        async with websockets.connect(self.GATEWAY_URL) as websocket:
            self.connection = websocket
            await self.identify()
            await self.listen()

    async def identify(self):
        """Authenticates with the Discord Gateway"""
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents.flags,
                "properties": {
                    "$os": "linux",
                    "$browser": "discord-lite",
                    "$device": "discord-lite"
                }
            }
        }
        await self.connection.send(json.dumps(payload))

    async def listen(self):
        """Listens for events from Discord Gateway"""
        try:
            async for message in self.connection:
                data = json.loads(message)
                await self.handle_event(data)
        except websockets.ConnectionClosed:
            print("Connection closed!")

    async def handle_event(self, data):
        """Processes events from Discord"""
        event_type = data.get('t')
        if event_type == "READY":
            if "on_ready" in self.event_handlers:
                await self.event_handlers["on_ready"]()
        # Additional events can be added here

    async def close(self):
        """Closes the WebSocket connection"""
        if self.connection:
            await self.connection.close()
