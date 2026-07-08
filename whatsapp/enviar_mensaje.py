"""
Enviar mensajes de WhatsApp con la Cloud API de Meta.

Uso rápido:
    1. Copia el archivo .env.example a .env y rellena tus datos.
    2. Instala dependencias:   pip install -r requirements.txt
    3. Ejecuta:

       # Enviar la plantilla de prueba "hello_world" (funciona siempre en pruebas):
       python enviar_mensaje.py --plantilla --para 34600111222

       # Enviar texto libre (solo si el destinatario te escribió en las últimas 24h):
       python enviar_mensaje.py --texto "Hola, esto es una prueba" --para 34600111222

Nota importante sobre las reglas de WhatsApp:
  - Con un número de PRUEBA solo puedes escribir a números que hayas
    registrado como "destinatarios" en el panel de Meta.
  - El TEXTO LIBRE solo se permite si el usuario te escribió en las últimas
    24 horas. Fuera de esa ventana debes usar una PLANTILLA aprobada
    (por eso incluimos la opción --plantilla con "hello_world").
"""

import argparse
import os
import sys

import requests
from dotenv import load_dotenv

# Carga las variables del archivo .env (tus credenciales)
load_dotenv()

TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
# Versión de la API de Meta. Puedes dejar la que viene por defecto.
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v21.0")


def _comprobar_credenciales():
    """Avisa de forma clara si faltan credenciales."""
    faltan = []
    if not TOKEN:
        faltan.append("WHATSAPP_TOKEN")
    if not PHONE_NUMBER_ID:
        faltan.append("WHATSAPP_PHONE_NUMBER_ID")
    if faltan:
        print("❌ Faltan estas variables en tu archivo .env: " + ", ".join(faltan))
        print("   Copia .env.example a .env y rellénalo. Mira GUIA.md paso a paso.")
        sys.exit(1)


def enviar_texto(para: str, texto: str) -> dict:
    """Envía un mensaje de texto libre a un número."""
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    cuerpo = {
        "messaging_product": "whatsapp",
        "to": para,
        "type": "text",
        "text": {"body": texto},
    }
    return _enviar(url, cuerpo)


def enviar_plantilla(para: str, nombre_plantilla: str = "hello_world",
                     idioma: str = "en_US") -> dict:
    """Envía una plantilla aprobada (por defecto la de prueba 'hello_world')."""
    url = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"
    cuerpo = {
        "messaging_product": "whatsapp",
        "to": para,
        "type": "template",
        "template": {
            "name": nombre_plantilla,
            "language": {"code": idioma},
        },
    }
    return _enviar(url, cuerpo)


def _enviar(url: str, cuerpo: dict) -> dict:
    """Hace la petición HTTP y muestra el resultado de forma amigable."""
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
    }
    respuesta = requests.post(url, headers=headers, json=cuerpo, timeout=30)

    if respuesta.ok:
        datos = respuesta.json()
        id_mensaje = datos.get("messages", [{}])[0].get("id", "(desconocido)")
        print(f"✅ Mensaje enviado. ID: {id_mensaje}")
        return datos

    # Si algo falla, mostramos el error que devuelve Meta (suele ser muy claro)
    print(f"❌ Error {respuesta.status_code} al enviar el mensaje:")
    try:
        error = respuesta.json().get("error", {})
        print(f"   Mensaje: {error.get('message')}")
        print(f"   Detalle: {error.get('error_data', {}).get('details', '')}")
    except Exception:
        print(f"   {respuesta.text}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Enviar mensajes de WhatsApp (Cloud API de Meta)")
    parser.add_argument("--para", required=True,
                        help="Número destino con código de país, sin '+'. Ej: 34600111222")
    grupo = parser.add_mutually_exclusive_group(required=True)
    grupo.add_argument("--texto", help="Texto libre a enviar")
    grupo.add_argument("--plantilla", action="store_true",
                       help="Enviar la plantilla de prueba 'hello_world'")
    parser.add_argument("--nombre-plantilla", default="hello_world",
                        help="Nombre de otra plantilla aprobada (opcional)")
    parser.add_argument("--idioma", default="en_US",
                        help="Código de idioma de la plantilla. Ej: es, en_US")
    args = parser.parse_args()

    _comprobar_credenciales()

    if args.plantilla:
        enviar_plantilla(args.para, args.nombre_plantilla, args.idioma)
    else:
        enviar_texto(args.para, args.texto)


if __name__ == "__main__":
    main()
