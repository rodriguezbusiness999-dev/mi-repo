"""Acceso a la API de Google Classroom."""
import os
from datetime import date

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.coursework.students",
]


def _servicio():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flujo = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flujo.run_local_server(port=0)
        with open("token.json", "w") as f:
            f.write(creds.to_json())
    return build("classroom", "v1", credentials=creds)


def listar_cursos() -> list[dict]:
    res = _servicio().courses().list(courseStates=["ACTIVE"], teacherId="me").execute()
    return res.get("courses", [])


def crear_tarea(course_id: str, titulo: str, descripcion: str, puntos: int,
                fecha_entrega: date | None = None, publicar: bool = False) -> dict:
    cuerpo = {
        "title": titulo,
        "description": descripcion,
        "workType": "ASSIGNMENT",
        "maxPoints": puntos,
        "state": "PUBLISHED" if publicar else "DRAFT",
    }
    if fecha_entrega:
        cuerpo["dueDate"] = {
            "year": fecha_entrega.year,
            "month": fecha_entrega.month,
            "day": fecha_entrega.day,
        }
        cuerpo["dueTime"] = {"hours": 23, "minutes": 59}  # hora UTC
    return _servicio().courses().courseWork().create(courseId=course_id, body=cuerpo).execute()
