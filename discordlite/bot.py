# discordlite/bot.py
import aiohttp
import asyncio

class Bot:
    def __init__(self):
        """
        Initializes the bot instance.
        """
        self.token = None
        self.session = None
        self.base_url = "https://discord.com/api/v10"
        self.loop = asyncio.get_event_loop()

    async def _authenticate(self):
        """
        Authenticates the bot using the provided token.
        """
        headers = {
            "Authorization": f"Bot {self.token}",
            "Content-Type": "application/json",
        }
        async with self.session.get(f"{self.base_url}/users/@me", headers=headers) as response:
            if response.status == 200:
                user_data = await response.json()
                print(f"Logged in as {user_data['username']}#{user_data['discriminator']}")
            else:
                raise Exception(f"Failed to authenticate: {response.status} - {await response.text()}")

    def login(self, token: str):
        """
        Logs the bot in using the given token.
        :param token: The bot token provided by Discord.
        """
        self.token = token
        self.session = aiohttp.ClientSession(loop=self.loop)
        try:
            self.loop.run_until_complete(self._authenticate())
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.loop.run_until_complete(self.session.close())
            self.session = None

# Example usage:
# if __name__ == "__main__":
#     bot = Bot()
#     bot.login("YOUR_BOT_TOKEN")
