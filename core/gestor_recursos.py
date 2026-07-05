import gc
import psutil
import asyncio
import os
from typing import Optional

class GestorRecursos:
    def __init__(self, limite_memoria=0.8, limite_cpu=0.7):
        self.limite_memoria = limite_memoria
        self.limite_cpu = limite_cpu
        self.hilos_activos = 0
        self.memoria_liberada = 0
        
    def verificar_recursos(self) -> dict:
        memoria = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=0.1)
        
        estado = {
            "memoria_uso": memoria.percent,
            "memoria_available": memoria.available / (1024**3),  # GB
            "cpu_uso": cpu,
            "necesita_ajuste": False,
            "accion": None
        }
        
        if memoria.percent > self.limite_memoria * 100:
            estado["necesita_ajuste"] = True
            estado["accion"] = "liberar_memoria"
            
        if cpu > self.limite_cpu * 100:
            estado["necesita_ajuste"] = True
            estado["accion"] = "reducir_hilos"
            
        return estado
        
    async def ajustar_recursos(self):
        estado = self.verificar_recursos()
        
        if estado["necesita_ajuste"]:
            if estado["accion"] == "liberar_memoria":
                self._liberar_memoria()
            elif estado["accion"] == "reducir_hilos":
                await self._reducir_hilos()
                
        return estado
        
    def _liberar_memoria(self):
        gc.collect()
        # Limpiar cache de sockets
        import socket
        socket.setdefaulttimeout(1)
        
    async def _reducir_hilos(self):
        self.hilos_activos = max(1, int(self.hilos_activos * 0.8))
        
    def obtener_recomendaciones(self) -> dict:
        memoria = psutil.virtual_memory()
        cpu_count = psutil.cpu_count()
        
        return {
            "max_hilos_recomendados": cpu_count * 100,
            "max_conexiones_recomendadas": int(memoria.available / (1024 * 1024) * 0.5),
            "usa_nginx": self._detectar_nginx(),
            "usa_cloudflare": self._detectar_cloudflare()
        }
        
    def _detectar_nginx(self) -> bool:
        return False
        
    def _detectar_cloudflare(self) -> bool:
        return False