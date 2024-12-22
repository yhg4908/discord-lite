import aiohttp
import asyncio
from typing import Optional

class DiscordLiteClient:
    def __init__(self):
        self._token: Optional[str] = None
        self._session: Optional[aiohttp.ClientSession] = None
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._heartbeat_interval: Optional[int] = None
        self._last_sequence: Optional[int] = None
        
    async def login(self, token: str) -> None:
        """
        Discord 봇을 로그인하고 WebSocket 연결을 수립합니다.
        
        Args:
            token (str): Discord 봇 토큰
            
        Raises:
            ValueError: 토큰이 비어있거나 유효하지 않은 경우
            ConnectionError: Discord API 연결 실패시
        """
        if not token or not isinstance(token, str):
            raise ValueError("유효한 토큰을 입력해주세요.")
            
        self._token = token
        
        try:
            self._session = aiohttp.ClientSession()
            
            # Gateway URL 가져오기
            async with self._session.get(
                'https://discord.com/api/v10/gateway'
            ) as response:
                if response.status != 200:
                    raise ConnectionError("Discord API 연결에 실패했습니다.")
                gateway_data = await response.json()
                
            # WebSocket 연결
            self._ws = await self._session.ws_connect(
                f"{gateway_data['url']}/?v=10&encoding=json"
            )
            
            # 식별 정보 전송
            await self._ws.send_json({
                "op": 2,
                "d": {
                    "token": self._token,
                    "properties": {
                        "os": "linux",
                        "browser": "discord-lite",
                        "device": "discord-lite"
                    },
                    "intents": 0  # 기본 인텐트 없음
                }
            })
            
            # 기본 이벤트 루프 시작
            asyncio.create_task(self._heartbeat_loop())
            asyncio.create_task(self._event_loop())
            
        except Exception as e:
            if self._session:
                await self._session.close()
            raise ConnectionError(f"연결 중 오류가 발생했습니다: {str(e)}")
            
    async def _heartbeat_loop(self) -> None:
        """Discord 서버와의 연결을 유지하기 위한 하트비트 전송"""
        while True:
            if self._heartbeat_interval:
                await self._ws.send_json({
                    "op": 1,
                    "d": self._last_sequence
                })
                await asyncio.sleep(self._heartbeat_interval / 1000)
                
    async def _event_loop(self) -> None:
        """WebSocket 이벤트 수신 및 처리"""
        async for msg in self._ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = msg.json()
                
                if data["op"] == 10:  # Hello
                    self._heartbeat_interval = data["d"]["heartbeat_interval"]
                elif data["op"] == 11:  # Heartbeat ACK
                    pass
                elif data["op"] == 0:  # Dispatch
                    self._last_sequence = data["s"]
                    
    async def close(self) -> None:
        """봇 연결 종료 및 리소스 정리"""
        if self._ws:
            await self._ws.close()
        if self._session:
            await self._session.close()
