from .client import DiscordLiteClient

__version__ = '0.1.0'

def login(token: str) -> DiscordLiteClient:
    """
    간단한 봇 로그인을 위한 헬퍼 함수
    
    사용 예시:
        bot = discord_lite.login('your_token_here')
    """
    client = DiscordLiteClient()
    asyncio.get_event_loop().run_until_complete(client.login(token))
    return client
