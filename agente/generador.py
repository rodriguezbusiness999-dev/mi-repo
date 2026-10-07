"""Genera el contenido de una tarea usando Claude."""
import json
import os

import anthropic

MODELO = os.environ.get("AGENTE_MODELO", "claude-sonnet-5-5")

PROMPT = """Eres un asistente para un profesor. Redacta una tarea para estudiantes.

Nivel/curso: {curso}
Tema: {tema}
Tipo de actividad: {tipo}
Puntos: {puntos}
Indicaciones extra del profesor: {extra}

Responde SOLO con un JSON válido con estas claves:
- "titulo": título corto de la tarea
- "descripcion": instrucciones claras para el estudiante (puede usar saltos de línea),
  incluyendo los criterios de evaluación y cómo se reparten los {puntos} puntos
"""


def generar_tarea(curso: str, tema: str, tipo: str, puntos: int, extra: str = "") -> dict:
    cliente = anthropic.Anthropic()  # usa ANTHROPIC_API_KEY
    respuesta = cliente.messages.create(
        model=MODELO,
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": PROMPT.format(
                curso=curso, tema=tema, tipo=tipo, puntos=puntos, extra=extra or "ninguna"
            ),
        }],
    )
    texto = respuesta.content[0].text.strip()
    if texto.startswith("```"):
        texto = texto.strip("`").removeprefix("json").strip()
    return json.loads(texto)
