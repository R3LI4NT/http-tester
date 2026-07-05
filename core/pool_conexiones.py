import asyncio
import aiohttp
from typing import Optional, Dict
from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector
import ssl

class PoolConexiones:
    def __init__(self, max_size=10000):
        self.max_size = max_size
        self.conexiones = {}
        self.activas = 0
        self.lock = asyncio.Lock()
        self.ssl_context = self._crear_contexto_ssl()
        self.sesiones_cerradas = []
        
    def _crear_contexto_ssl(self):
        contexto = ssl.create_default_context()
        contexto.check_hostname = False
        contexto.verify_mode = ssl.CERT_NONE
        contexto.set_ciphers('ALL:!aNULL:!eNULL:!LOW:!EXP:!RC4:!3DES:!MD5:!PSK:!SRP:!DSS:!SEED:!IDEA:!ECDSA:!kRSA')
        return contexto
        
    async def obtener_conexion(self, host, puerto, ssl=True, proxy=None):
        async with self.lock:
            if self.activas >= self.max_size:
                return None
                
            clave = f"{host}:{puerto}:{proxy if proxy else 'directo'}"
            
            if clave in self.conexiones:
                sesion = self.conexiones[clave]
                if not sesion.closed:
                    self.activas += 1
                    return sesion
                else:
                    del self.conexiones[clave]
            
            connector = None
            if proxy:
                try:
                    connector = ProxyConnector.from_url(
                        f"socks5://{proxy}",
                        ssl=self.ssl_context if ssl else False
                    )
                except:
                    connector = TCPConnector(
                        limit=0,
                        ttl_dns_cache=300,
                        ssl=self.ssl_context if ssl else False,
                        enable_cleanup_closed=True,
                        force_close=True
                    )
            else:
                connector = TCPConnector(
                    limit=0,
                    ttl_dns_cache=300,
                    ssl=self.ssl_context if ssl else False,
                    enable_cleanup_closed=True,
                    force_close=True
                )
            
            sesion = ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=5, connect=3),
                trust_env=True
            )
            
            self.conexiones[clave] = sesion
            self.activas += 1
            return sesion
            
    async def liberar_conexion(self, sesion):
        async with self.lock:
            self.activas -= 1
            if sesion and not sesion.closed:
                try:
                    await sesion.close()
                except:
                    pass
            self.sesiones_cerradas.append(sesion)
            
    async def limpiar(self):
        async with self.lock:
            for clave, sesion in list(self.conexiones.items()):
                if not sesion.closed:
                    try:
                        await sesion.close()
                    except:
                        pass
            self.conexiones.clear()
            self.activas = 0
            self.sesiones_cerradas.clear()
            
    def conexiones_activas(self):
        return self.activas