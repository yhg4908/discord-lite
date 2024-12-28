import asyncio
from .gateway import Gateway
from .http import HTTPClient

class Bot:
    """Lightweight Discord bot"""
    def __init__(self, prefix: str, intents):
        self.prefix = prefix
        self.intents = intents
        self.token = None
        self.gateway = None
        self.http = None
        self.event_handlers = {}  # Stores event handlers

    def add_event(self, event_name: str, handler):
        """Registers an event handler"""
        if not asyncio.iscoroutinefunction(handler):
            raise TypeError(f"Handler for {event_name} must be a coroutine function")
        self.event_handlers[event_name] = handler

    def run(self, token: str):
        """Runs the bot"""
        self.token = token
        self.http = HTTPClient(token)
        self.gateway = Gateway(token, self.intents, self.event_handlers)

        # Use asyncio.run to start the async loop
        asyncio.run(self._run_bot())

    async def _run_bot(self):
        """Internal async method to run the bot"""
        try:
            await self.gateway.connect()
        except KeyboardInterrupt:
            await self.gateway.close()
