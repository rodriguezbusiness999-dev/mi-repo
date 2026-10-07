# mi-repo

Repositorio de prueba para practicar el flujo de Pull Requests con GitHub.

## Primeros pasos

1. Clona este repositorio:
   ```bash
   git clone https://github.com/rodriguezbusiness999-dev/mi-repo.git
   ```
2. Crea una rama para tus cambios:
   ```bash
   git checkout -b mi-rama
   ```
3. Haz tus cambios, confirma y abre un Pull Request.

## Contribuir

Las contribuciones son bienvenidas. Por favor abre un issue antes de enviar cambios importantes.

## Agente para Google Classroom (profesores)

Genera tareas con IA (Claude) y las sube a Google Classroom como **borrador**, para que las revises antes de publicarlas.

### Configuración
1. `pip install -r requirements.txt`
2. En [Google Cloud Console](https://console.cloud.google.com/): activa la **Classroom API**, crea credenciales *OAuth (aplicación de escritorio)* y guarda el archivo como `credentials.json` en la raíz (está en `.gitignore`).
3. `export ANTHROPIC_API_KEY=...`

### Uso
```bash
python -m agente cursos
python -m agente crear --curso-id ID --nivel "3º secundaria" --tema "Fracciones" --fecha 2026-10-20
```
Añade `--publicar` solo si quieres saltarte la revisión.
