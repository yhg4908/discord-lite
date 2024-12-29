import asyncio
from .gateway import Gateway
from .http import HTTPClient

class Bot:
    PERMISSIONS = {
        "ADMINISTRATOR": 1 << 3,
        "MANAGE_MESSAGES": 1 << 13,
    }

    def __init__(self, prefix: str, intents):
        self.prefix = prefix
        self.intents = intents
        self.token = None
        self.gateway = None
        self.http = None
        self.event_handlers = {}
        self.commands = {}
        self.command_permissions = {}  # 명령어별 권한 제한
        self.command_roles = {}        # 명령어별 역할 제한

    def add_event(self, event_name: str, handler):
        self.event_handlers[event_name] = handler

    def add_command(self, command_name: str, handler, required_permissions=None, required_roles=None):
        """Adds a command with optional permissions or role restrictions"""
        self.commands[command_name] = handler
        if required_permissions:
            self.command_permissions[command_name] = required_permissions
        if required_roles:
            self.command_roles[command_name] = required_roles

    def has_permission(self, user_permissions, required_permissions):
        """Checks if user has required permissions"""
        return (user_permissions & required_permissions) == required_permissions

    def has_role(self, user_roles, required_roles):
        """Checks if user has one of the required roles"""
        return any(role in user_roles for role in required_roles)

    def run(self, token: str):
        """Runs the bot"""
        self.token = token
        self.http = HTTPClient(token)
        asyncio.run(self._initialize_and_run())

    async def _initialize_and_run(self):
        """Initializes HTTP client and starts gateway connection"""
        await self.http.initialize()
        self.gateway = Gateway(self.token, self.intents, self.event_handlers, self.commands, self.prefix, self.http)
        try:
            await self.gateway.connect()
        except KeyboardInterrupt:
            await self.gateway.close()
            await self.http.close()

    async def send_message(self, channel_id: str, content: str, file_paths: list = None):
        """Sends a message with optional file attachments"""
        await self.http.send_message(channel_id, content, file_paths)
