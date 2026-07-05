# 🔥 HTTP-TESTER

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


<p align="center">
    <b>⚠️ ADVERTENCIA: Esta herramienta es para fines educativos y de pruebas autorizadas únicamente.</b>
</p>
