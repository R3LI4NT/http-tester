import random
import os

AGENTES_USUARIO = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G975U) AppleWebKit/537.36 Chrome/88.0.4324.68 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 coc_coc_browser/87.0.144 Chrome/81.0.4044.144",
    "Mozilla/5.0 (Linux; Android 9; SM-N950U) AppleWebKit/537.36 Chrome/81.0.4044.138 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi 6A) AppleWebKit/537.36 Chrome/95.0.4638.74 Mobile Safari/537.36",
    "Dalvik/2.1.0 (Linux; U; Android 10; MI CC 9 MIUI/V11.0.1.0.QFCCNXM)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) Mobile/15E148 YaBrowser/19.5.2.38.10",
    "Mozilla/5.0 (Windows NT 10.5; Win64; x64) AppleWebKit/536.26 Chrome/49.0.1659.324 Safari/602",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (Linux; U; Android 5.1.1; MOTO XT1575) AppleWebKit/537.38 Chrome/47.0.2776.198 Mobile",
    "Mozilla/5.0 (Windows; Windows NT 6.3; x64) AppleWebKit/533.12 Chrome/47.0.1912.319 Edge/12.46260",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Edge/118.0.2088.76",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Edge/118.0.2088.76",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.6167.85 Safari/537.36 Edg/121.0.2277.83",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148",
    "Mozilla/5.0 (Linux; Android 14; SM-S918U) AppleWebKit/537.36 Chrome/121.0.6167.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 Chrome/121.0.6167.85 Mobile Safari/537.36"
]

IDIOMAS = [
    "en-US,en;q=0.9",
    "es-ES,es;q=0.9",
    "fr-FR,fr;q=0.9",
    "de-DE,de;q=0.9",
    "it-IT,it;q=0.9",
    "pt-BR,pt;q=0.9",
    "ja-JP,ja;q=0.9",
    "zh-CN,zh;q=0.9",
    "ru-RU,ru;q=0.9",
    "ar-SA,ar;q=0.9"
]

TIPOS_CONTENIDO = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "application/json,text/plain,*/*",
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
]

def generar_cabeceras_aleatorias():
    return {
        "User-Agent": random.choice(AGENTES_USUARIO),
        "Accept": random.choice(TIPOS_CONTENIDO),
        "Accept-Language": random.choice(IDIOMAS),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate", "br"]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Cache-Control": random.choice(["no-cache", "max-age=0", "no-store"]),
        "Pragma": "no-cache",
        "Sec-Ch-Ua": f'"Chromium";v="{random.randint(118, 121)}", "Google Chrome";v="{random.randint(118, 121)}", "Not-A.Brand";v="99"',
        "Sec-Ch-Ua-Mobile": random.choice(["?0", "?1"]),
        "Sec-Ch-Ua-Platform": random.choice(['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"']),
        "Sec-Fetch-Dest": random.choice(["document", "empty", "script", "style", "image"]),
        "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors", "same-origin"]),
        "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site"]),
        "Sec-Fetch-User": random.choice(["?1", "?0"])
    }