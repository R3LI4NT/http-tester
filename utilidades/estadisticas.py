import time
from threading import Lock

class GestorEstadisticas:
    def __init__(self):
        self.total = 0
        self.exitos = 0
        self.errores = 0
        self.ancho_banda = 0
        self.inicio = time.time()
        self.lock = Lock()
        
    def agregar_exito(self, bytes_enviados=0):
        with self.lock:
            self.total += 1
            self.exitos += 1
            self.ancho_banda += bytes_enviados
            
    def agregar_error(self):
        with self.lock:
            self.total += 1
            self.errores += 1
            
    def obtener_todo(self):
        with self.lock:
            return self.total, self.exitos, self.errores, self.ancho_banda
            
    def transcurrido(self):
        return time.time() - self.inicio
        
    def tasa(self):
        transcurrido = self.transcurrido()
        if transcurrido > 0:
            return self.total / transcurrido
        return 0
        
    def reset(self):
        with self.lock:
            self.total = 0
            self.exitos = 0
            self.errores = 0
            self.ancho_banda = 0
            self.inicio = time.time()