# Proceso de Selección: Desarrollo Web / Líder Técnico - Laboratorio de Ciencia de Datos ADA

## Prueba técnica ADA: mantenimiento e integración de un sistema heredado

Un equipo de desarrolladores junior construyó parcialmente una API de seguimiento de proyectos.
Usted se incorpora como responsable técnico. Revise el sistema, complete el resumen
de proyecto y corrija los problemas prioritarios. El código y sus pruebas necesitan
revisión; una prueba que pasa no demuestra por sí sola que el comportamiento sea correcto.
Todos los datos y credenciales del ejercicio son ficticios.

## Alcance y tiempo

Tiempo de trabajo: 180 minutos, después de disponer de Python 3.12, Node.js y las dependencias.
Reserve unos 20 minutos para documentar. No se espera resolver toda la deuda.
La descarga inicial de imágenes/dependencias y problemas de infraestructura ajenos
al candidato no consumen tiempo de evaluación. Se permite documentación, Internet,
ChatGPT, Claude Code, Gemini y otros asistentes. Declare su uso en DECISIONS.md.

El alcance incluye backend Python/FastAPI, MongoDB, Docker y un dashboard pequeño
en Angular 21. El frontend es obligatorio; se proporciona un esqueleto compilable
para dedicar el tiempo a integración y comportamiento, no a crear el proyecto.

## Ejecución local

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Los tests usan mongomock y no requieren MongoDB ni Docker. Para ejecutar la API real,
inicie una instancia local de MongoDB en el puerto 27017 y ejecute:

```bash
python -m scripts.seed
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Documentación interactiva: http://localhost:8000/docs.
También se proporciona `docker compose up --build`. Su configuración forma parte
 de la revisión; el arranque de contenedores no garantiza conectividad funcional.
Después de corregirlo, cargue datos con `docker compose exec api python -m scripts.seed`.
`.env.example` documenta variables previstas; compruebe su uso efectivo.

## Contrato esperado

IDs: cadenas hexadecimales de ObjectId de 24 caracteres. ID inválido: HTTP 422;
entidad inexistente: 404. Una indisponibilidad de persistencia debe devolver 503,
sin detalles internos, y quedar registrada en logs. Los cambios no deben romper
los casos válidos existentes. Se permite cambiar organización interna y añadir dependencias.
No se exige una estructura particular de capas.

| Método y ruta | Comportamiento esperado |
|---|---|
| GET /health | 200, señal de proceso vivo; no certifica disponibilidad de DB |
| GET /projects?status=active | 200, lista; filtro opcional active o archived; otro valor 422 |
| POST /projects | 201; nombre no vacío tras strip, máximo 120 caracteres; presupuesto numérico finito ≥0; status active o archived |
| GET /projects/{id} | 200; id, name, budget numérico, status; no exponer _id ni metadata |
| DELETE /projects/{id} | 200 y {"deleted":true}; eliminar también sus actividades; 404 si no existe |
| POST /projects/{id}/activities | 201; comprobar proyecto; title no vacío tras strip, máximo 120; hours finitas ≥0; completed booleano |
| GET /projects/{id}/activities | 200 lista; 404 si no existe proyecto, incluso si lista vacía |
| GET /projects/{id}/summary | 200 con contrato definido abajo |
| GET /reports/portfolio | 200 con token correcto en X-Report-Token; 401 en otro caso; conservar formato y cálculos válidos existentes |

Rechace booleanos como budget/hours. No se exige unicidad de nombres ni autenticación
general; el token de reportes sirve solo para revisar configuración. No añada correo,
servicios externos ni nuevas funciones. Mantenga los nombres de campos del contrato.

## Funcionalidad por completar

`GET /projects/{id}/summary` debe devolver exactamente estos campos:

```json
{
  "project_id": "64b000000000000000000001",
  "name": "SAT",
  "activity_count": 3,
  "completed_count": 2,
  "total_hours": 35.0,
  "completion_rate": 0.6666666666666666
}
```

completion_rate = completed_count / activity_count, entre 0 y 1; si no hay
actividades, todos los indicadores son cero. total_hours suma todas las actividades,
completadas o no. No mezcle actividades de otros proyectos. Se aceptan diferencias
de redondeo de 1e-6. El proyecto Chatbots de la fixture no tiene actividades.

## Dashboard Angular 21 (obligatorio)

Se proporciona `frontend/` con Angular 21.0.0, componentes standalone, tipos,
HttpClient, selector y tarjetas. La consulta de lista está implementada; la consulta
del resumen y su manejo de estados están pendientes. No sustituya Angular por otro framework.

Requisitos de entorno: Node.js 22.12+ de la rama 22 o Node.js 24; TypeScript 5.9.
Las versiones están fijadas en package.json y package-lock.json.

```bash
cd frontend
npm ci
npm start
```

Abra http://localhost:4200. El proxy de desarrollo dirige `/api/**` al backend en
http://127.0.0.1:8000 y elimina el prefijo `/api`; las rutas FastAPI no cambian.
Para otro servidor, cambie el destino del proxy y reinicie ng serve. No incruste
credenciales ni el token privado de reportes en el navegador. El proxy evita necesitar
CORS en desarrollo; no es una configuración de despliegue para producción.

Complete estos comportamientos:

- Obtener proyectos de GET /projects; mostrar carga, lista vacía y fallo de lista.
- Al seleccionar un proyecto, consultar GET /projects/{id}/summary y mostrar
  nombre, cantidad de actividades, completadas, horas y avance en porcentaje.
- Mostrar carga y error visible del resumen, con una acción para reintentar.
- Al cambiar o deseleccionar proyecto, no mostrar indicadores de la selección anterior.
  Si hay respuestas fuera de orden, la interfaz debe conservar la última selección.
- Mostrar ceros correctamente cuando el proyecto no tiene actividades.
- Mantener una interfaz legible en móvil y escritorio, con etiquetas accesibles.
- Añadir al menos dos pruebas automatizadas de frontend: una de integración HTTP
  del servicio/flujo y otra de error o cambio de selección. Se permite elegir el runner;
  documente cómo ejecutarlas. Las pruebas deben ejercitar código productivo.

No se piden gráficas, login, CRUD visual, librerías de UI ni diseño sofisticado.
Los datos deben proceder del backend real: no usar fixtures incrustadas como solución.
Mocks son válidos exclusivamente en pruebas. Dockerizar el frontend es opcional;
la ejecución local con npm es suficiente, y `npm run build` debe funcionar.

Aceptación con la fixture: SAT debe mostrar 3 actividades, 2 completadas, 35 horas y
66.7 % aproximadamente; Chatbots, ceros. Demuestre el flujo navegador → FastAPI →
MongoDB, y documente la verificación en DECISIONS.md. Incluya una captura del dashboard
con datos reales y evidencia del manejo de un error.

## Tareas y entrega

1. Ejecute la suite y describa arquitectura y estado inicial.
2. Complete el resumen y corrija comportamientos que incumplan el contrato.
3. Documente hasta cinco problemas prioritarios, con evidencia e impacto.
4. Refactorice un componente y agregue pruebas de regresión y casos negativos.
5. Prepare configuración y Docker para ejecución reproducible.
6. Complete el dashboard Angular 21 y pruebe su integración con el backend.
7. Complete DECISIONS.md con cambios, verificación, pendientes y continuidad del equipo.

Entregue la solución en un repositorio Git público, con instrucciones reproducibles y DECISIONS.md.  No incluya
entornos virtuales, datos personales ni credenciales reales. No cambie pruebas para
ocultar fallos; puede reemplazar pruebas deficientes explicando por qué. La evaluación
privilegia correctitud, pruebas útiles, criterio y mantenibilidad. No se premia volumen
 de código ni número de problemas cosméticos. Documente lo que no logró terminar.

## Estructura

```text
frontend/          dashboard Angular 21 y proxy de desarrollo
app/               API, modelos, configuración y conexión MongoDB
scripts/seed.py    fixture idempotente de proyectos y actividades
tests/             pruebas públicas y fixtures aisladas
requirements.txt   dependencias de ejecución y pruebas
pytest.ini         configuración de pytest
Dockerfile         imagen de la API
compose.yaml       API y MongoDB
.env.example       configuración prevista
DECISIONS.md       informe del candidato
```


## Inventario completo

```text
.dockerignore
.env.example
.gitignore
DECISIONS.md
Dockerfile
README.md
app/__init__.py
app/config.py
app/database.py
app/main.py
app/models.py
compose.yaml
frontend/angular.json
frontend/package-lock.json
frontend/package.json
frontend/proxy.conf.json
frontend/src/app/app.component.html
frontend/src/app/app.component.ts
frontend/src/app/project.models.ts
frontend/src/app/projects.service.ts
frontend/src/index.html
frontend/src/main.ts
frontend/src/styles.css
frontend/tsconfig.app.json
frontend/tsconfig.json
pytest.ini
requirements.txt
scripts/__init__.py
scripts/seed.py
tests/conftest.py
tests/test_api.py
```
