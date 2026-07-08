# Guía: enviar mensajes de WhatsApp paso a paso

Esta guía te lleva desde cero hasta enviar tu primer mensaje de WhatsApp con la
**Cloud API de Meta** (la oficial y gratuita para pruebas).

---

## Paso 1 — Crear tu cuenta de desarrollador en Meta

1. Entra a **https://developers.facebook.com** y pulsa **"Comenzar"** (arriba a la derecha).
2. Inicia sesión con tu cuenta de **Facebook** (si no tienes, créala; es gratis).
3. Verifica tu cuenta con tu número de móvil y correo cuando te lo pida.

> 👉 **"Dónde inicias sesión" es aquí**: en developers.facebook.com con tu cuenta de Facebook.

---

## Paso 2 — Crear una App

1. Ve a **https://developers.facebook.com/apps** y pulsa **"Crear app"**.
2. En el tipo de app elige **"Otro"** → **"Empresa / Business"**.
3. Ponle un nombre (ej. `mis-flujos-whatsapp`) y créala.

---

## Paso 3 — Añadir el producto WhatsApp

1. Dentro de tu app, en la lista de productos busca **"WhatsApp"** y pulsa **"Configurar"**.
2. Meta te dará automáticamente:
   - Un **número de teléfono de PRUEBA** (no es tu número real, es de Meta).
   - Un **Phone number ID** (un número largo).
   - Un **token de acceso temporal**.

Esta pantalla se llama **"API Setup"** (Configuración de la API). Déjala abierta,
de aquí copiarás los datos.

---

## Paso 4 — Registrar tu número personal como destinatario de prueba

Con un número de prueba **solo puedes escribir a números autorizados**:

1. En la misma pantalla "API Setup", busca **"To"** (Para) → **"Manage phone number list"**.
2. Añade **tu propio número de móvil** de WhatsApp.
3. Te llegará un código por WhatsApp para confirmarlo. Introdúcelo.

Ahora tu móvil ya puede recibir mensajes de prueba. ✅

---

## Paso 5 — Copiar tus credenciales al proyecto

1. En este proyecto, copia el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```
2. Abre `.env` y pega:
   - `WHATSAPP_TOKEN` → el **token de acceso temporal** del paso 3.
   - `WHATSAPP_PHONE_NUMBER_ID` → el **Phone number ID** del paso 3.

> ⚠️ El token temporal **caduca en 24 horas**. Para uno permanente mira el
> apartado "Token permanente" más abajo.

---

## Paso 6 — Instalar y enviar tu primer mensaje

1. Instala las dependencias (solo la primera vez):
   ```bash
   pip install -r requirements.txt
   ```
2. Envía la plantilla de prueba a tu propio número (cámbialo por el tuyo, con
   código de país y **sin** el `+`):
   ```bash
   python enviar_mensaje.py --plantilla --para 34600111222
   ```
3. ¡Mira tu WhatsApp! Deberías recibir un mensaje "Hello World". 🎉

---

## Enviar texto libre (mensajes personalizados)

WhatsApp solo permite **texto libre** si la persona te escribió en las
**últimas 24 horas**. Prueba así:

1. Desde tu móvil, envía cualquier mensaje al número de prueba de Meta.
2. Antes de que pasen 24 horas, ejecuta:
   ```bash
   python enviar_mensaje.py --texto "Hola 👋 esto es una notificación de prueba" --para 34600111222
   ```

Para mandar mensajes **fuera** de esa ventana de 24h (por ejemplo recordatorios
automáticos), tendrás que crear y aprobar tus propias **plantillas** en el panel
de Meta (WhatsApp → Manage templates). Cuando llegues a ese punto, avísame y te
ayudo a montarlas.

---

## Token permanente (para no reconfigurar cada día)

El token de prueba caduca en 24h. Para uno que no caduque:

1. Ve a **business.facebook.com** → **Configuración del negocio** → **Usuarios** →
   **Usuarios del sistema**.
2. Crea un usuario del sistema, asígnale tu app y genera un token con los
   permisos `whatsapp_business_messaging` y `whatsapp_business_management`.
3. Pega ese token en `WHATSAPP_TOKEN` de tu `.env`.

(Este paso es un poco más avanzado; cuando quieras lo hacemos juntos.)

---

## ¿Y ahora qué?

Cuando ya envíes mensajes, los siguientes pasos naturales son:
- **Recibir** mensajes (webhook) para crear respuestas automáticas.
- **Plantillas** personalizadas para notificaciones programadas.
- Automatizar envíos (recordatorios, confirmaciones, etc.).

Pídemelo y lo vamos construyendo poco a poco.
