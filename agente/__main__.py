"""Uso:
  python -m agente cursos
  python -m agente crear --curso-id ID --tema "Fracciones" --fecha 2026-10-20
  python -m agente crear ... --publicar     # sin revisión previa (por defecto: borrador)
"""
import argparse
from datetime import date

from . import classroom, generador


def main():
    p = argparse.ArgumentParser(prog="agente")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("cursos", help="Lista tus cursos y sus IDs")

    c = sub.add_parser("crear", help="Genera una tarea con IA y la sube a Classroom")
    c.add_argument("--curso-id", required=True)
    c.add_argument("--nivel", default="", help="Ej: 3º de secundaria")
    c.add_argument("--tema", required=True)
    c.add_argument("--tipo", default="tarea individual")
    c.add_argument("--puntos", type=int, default=100)
    c.add_argument("--fecha", help="Fecha de entrega AAAA-MM-DD")
    c.add_argument("--extra", default="", help="Indicaciones adicionales")
    c.add_argument("--publicar", action="store_true", help="Publicar directo (por defecto queda en borrador)")
    a = p.parse_args()

    if a.cmd == "cursos":
        for curso in classroom.listar_cursos():
            print(f"{curso['id']}\t{curso['name']}")
        return

    tarea = generador.generar_tarea(a.nivel, a.tema, a.tipo, a.puntos, a.extra)
    print(f"\n=== {tarea['titulo']} ===\n{tarea['descripcion']}\n")
    fecha = date.fromisoformat(a.fecha) if a.fecha else None
    res = classroom.crear_tarea(a.curso_id, tarea["titulo"], tarea["descripcion"],
                                a.puntos, fecha, a.publicar)
    estado = "publicada" if a.publicar else "guardada como BORRADOR (revísala en Classroom)"
    print(f"Tarea {estado}: {res.get('alternateLink', res['id'])}")


main()
