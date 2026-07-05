import random
import aiofiles
from typing import List, Optional

class GestorProxies:
    def __init__(self, archivo=None):
        self.proxies = []
        if archivo:
            self.cargar_desde_archivo(archivo)
            
    def cargar_desde_archivo(self, archivo):
        try:
            with open(archivo, 'r') as f:
                for linea in f:
                    linea = linea.strip()
                    if linea and not linea.startswith('#'):
                        self.proxies.append(linea)
        except:
            pass
            
    def obtener_aleatorio(self) -> Optional[str]:
        if not self.proxies:
            return None
        return random.choice(self.proxies)
        
    def obtener_todos(self) -> List[str]:
        return self.proxies.copy()
        
    def agregar(self, proxy):
        if proxy not in self.proxies:
            self.proxies.append(proxy)
            
    def eliminar(self, proxy):
        if proxy in self.proxies:
            self.proxies.remove(proxy)
            
    def __len__(self):
        return len(self.proxies)