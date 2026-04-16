import asyncio
import json
import logging
import websockets
import time
from contextlib import contextmanager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

LAVALINK_URI = "ws://lavalink.sang0023.io.vn:443"
LAVALINK_PASSWORD = "lavalink"
RECONNECT_DELAY = 5
MAX_RECONNECT_DELAY = 60
HEARTBEAT_INTERVAL = 30  # Gửi heartbeat mỗi 30 giây
SESSION_TIMEOUT = 60  # Session timeout nếu không có data trong 60 giây

class LavalinkManager:
    def __init__(self):
        self.ws = None
        self.last_heartbeat = 0
        self.session_id = None
        self.connected = False

    async def send_heartbeat(self):
        """Gửi heartbeat để giữ kết nối sống."""
        if self.ws and not self.ws.closed:
            try:
                # Gửi ping để server biết client vẫn còn
                pong = await self.ws.ping()
                await pong
                self.last_heartbeat = time.time()
                logging.debug("💓 Heartbeat sent")
            except Exception as e:
                logging.warning(f"⚠️ Heartbeat error: {e}")

    async def recv_loop(self):
        """Nhận dữ liệu từ Lavalink với heartbeat monitor."""
        heartbeat_task = None
        try:
            async for msg in self.ws:
                if isinstance(msg, bytes):
                    logging.debug(f"Received bytes ({len(msg)} bytes).")
                else:
                    try:
                        data = json.loads(msg)
                        logging.info(f"📨 Received: {data.get('op', 'unknown')} op")
                        
                        # Track session ID
                        if data.get('op') == 'ready':
                            self.session_id = data.get('sessionId')
                            logging.info(f"✅ Session ID: {self.session_id}")
                    except Exception as e:
                        logging.warning(f"Error parsing JSON: {e}")
                        logging.debug(f"Raw message: {msg}")
        except asyncio.CancelledError:
            logging.debug("recv_loop cancelled")
            raise
        except websockets.ConnectionClosed as cc:
            logging.warning(f"🔌 WebSocket closed: {cc.code} - {cc.reason}")
            raise
        except Exception as e:
            logging.exception("❌ Error in recv_loop")
            raise
        finally:
            if heartbeat_task:
                heartbeat_task.cancel()

    async def heartbeat_loop(self):
        """Background task gửi heartbeat định kỳ."""
        try:
            while True:
                await asyncio.sleep(HEARTBEAT_INTERVAL)
                await self.send_heartbeat()
        except asyncio.CancelledError:
            logging.debug("heartbeat_loop cancelled")

    async def connect(self):
        """Kết nối tới Lavalink với enhanced error handling."""
        try:
            logging.info("🔌 Kết nối tới Lavalink...")
            self.ws = await websockets.connect(
                LAVALINK_URI,
                extra_headers={"Authorization": LAVALINK_PASSWORD},
                close_timeout=10,
                ping_interval=20,
                ping_timeout=5
            )
            logging.info("✅ Đã kết nối Lavalink!")
            self.connected = True
            self.last_heartbeat = time.time()
            
            # Khởi động heartbeat background task
            heartbeat_task = asyncio.create_task(self.heartbeat_loop())
            
            try:
                await self.recv_loop()
            finally:
                heartbeat_task.cancel()
                try:
                    await heartbeat_task
                except asyncio.CancelledError:
                    pass
            
        except websockets.ConnectionClosed as e:
            self.connected = False
            logging.warning(f"⚠️ Mất kết nối Lavalink ({e.code}): {e.reason}")
        except websockets.InvalidURI as e:
            self.connected = False
            logging.error(f"❌ Invalid URI: {e}")
        except Exception as e:
            self.connected = False
            logging.exception(f"❌ Connection error: {e}")

async def keep_connection():
    """Giữ kết nối tới Lavalink và tự reconnect nếu mất kết nối."""
    manager = LavalinkManager()
    reconnect_delay = RECONNECT_DELAY
    
    while True:
        try:
            await manager.connect()
            reconnect_delay = RECONNECT_DELAY  # Reset delay khi kết nối thành công
        except Exception as e:
            logging.exception(f"❌ Unexpected error: {e}")
        
        logging.info(f"🕒 Thử kết nối lại sau {reconnect_delay} giây...")
        await asyncio.sleep(reconnect_delay)
        
        # Exponential backoff (tăng delay từ từ)
        reconnect_delay = min(reconnect_delay * 1.5, MAX_RECONNECT_DELAY)

def main():
    try:
        logging.info("🎵 Khởi động Lavalink Connection Manager...")
        asyncio.run(keep_connection())
    except KeyboardInterrupt:
        logging.info("🛑 Dừng thủ công, thoát chương trình.")
    except Exception as e:
        logging.exception(f"❌ Fatal error: {e}")

if __name__ == "__main__":
    main()