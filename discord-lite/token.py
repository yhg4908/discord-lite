import requests
import asyncio

class Bot:
    def __init__(self):
        self.token = None
        self.base_url = "https://discord.com/api/v10"
        self.loop = asyncio.get_event_loop()

    def login(self, token: str):
        """
        Logs the bot into Discord using the provided token.

        :param token: The bot token as a string.
        """
        self.token = token
        try:
            response = requests.get(
                f"{self.base_url}/users/@me",
                headers={"Authorization": f"Bot {self.token}"}
            )
            if response.status_code == 200:
                print("[INFO] Bot successfully logged in.")
                print(f"[INFO] Logged in as: {response.json()['username']}#{response.json()['discriminator']}")
            elif response.status_code == 401:
                raise ValueError("Invalid token provided. Please check your token.")
            else:
                raise ConnectionError(f"Unexpected error occurred: {response.status_code} {response.text}")
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to connect to Discord API: {e}")

    async def start(self):
        """
        Starts the bot's main event loop.
        """
        if not self.token:
            raise RuntimeError("Cannot start the bot without logging in. Call 'login' first.")
        print("[INFO] Bot is online and ready!")
        while True:
            await asyncio.sleep(1)
