import aiohttp

class HTTPClient:
    """Handles HTTP requests to Discord API"""
    BASE_URL = "https://discord.com/api/v10"

    def __init__(self, token):
        self.token = token
        self.session = None

    async def initialize(self):
        """Initializes the aiohttp session"""
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bot {self.token}"}
        )

    async def request(self, method, endpoint, **kwargs):
        """Sends HTTP requests to Discord API"""
        if not self.session:
            raise Exception("HTTPClient session is not initialized. Call `initialize()` first.")
        url = f"{self.BASE_URL}{endpoint}"
        async with self.session.request(method, url, **kwargs) as response:
            if response.status != 200:
                raise Exception(f"HTTP error {response.status}: {await response.text()}")
            return await response.json()

    async def close(self):
        """Closes the HTTP session"""
        if self.session:
            await self.session.close()
