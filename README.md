# Proceso de Selección: Desarrollo Web / Líder Técnico - Laboratorio de Ciencia de Datos ADA

## Prueba técnica: del repositorio heredado al dashboard desplegado

## Objetivo del sistema

El sistema permite a la coordinación de un laboratorio consultar el estado de las
actividades de sus proyectos desde un dashboard web. Cada proyecto tiene un nombre,
presupuesto y estado; sus actividades registran título, horas estimadas y si están
completadas. Al seleccionar un proyecto, el dashboard muestra cantidad de actividades,
cantidad completada, horas totales y proporción de actividades completadas.

La finalidad es disponer de una vista sencilla para seguimiento y conversación con
el equipo. El avance representa actividades completadas / actividades totales:
no está ponderado por horas ni mide impacto o ejecución presupuestaria. Las horas
son la suma de las horas registradas, tanto completadas como pendientes.

Los datos ficticios incluyen SAT y Chatbots. La información se almacena en MongoDB,
FastAPI la consulta y calcula los indicadores, y Angular 21 los presenta. La entrega
debe demostrar el flujo completo navegador → API → MongoDB en la nube.

## Escenario de la prueba

Un equipo de desarrolladores junior (estudiantes) dejó este repositorio parcialmente construido. Usted se
incorpora como responsable técnico. Complete el flujo obligatorio y revise críticamente
el código heredado: algunas implementaciones y pruebas parecen correctas, pero necesitan
verificación. No se espera resolver toda la deuda técnica.

## Alcance y tiempo

Objetivo: 180 minutos de trabajo; reserve unos 20 minutos para documentar.
Python 3.12, Node.js 22.12+ de la rama 22 o Node.js 24 y cuentas Render y MongoDB Atlas
preparadas antes de iniciar. Descargas iniciales, esperas de despliegue e incidencias
del proveedor no consumen tiempo de trabajo. El tiempo debe confirmarse en un piloto.
Se permiten documentación, Internet, ChatGPT, Claude Code, Gemini y otros asistentes;
registre brevemente su uso y cómo verificó una modificación.

Solo se exige completar GET /projects y GET /projects/{id}/summary, el dashboard y
el despliegue. GET /health está preparado. El código heredado de creación, eliminación,
actividades individuales y reportes permanece como material de revisión, pero sus
funciones no están publicadas como rutas y no necesitan corrección obligatoria.
Docker/Compose se conservan como material opcional; no se exige repararlos.

## Preparación y ejecución local

Desde la raíz del repositorio:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

Los tests usan mongomock y no requieren MongoDB. Para la API real, conecte una base
de prueba local o Atlas, adapte la configuración y ejecute:

```bash
python -m scripts.seed
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

La configuración inicial usa localhost y debe adaptarse para respetar variables de
entorno. `.env.example` sirve de referencia; no implica que la aplicación ya las lea
ni que cargue automáticamente un archivo .env. Puede exportar las variables en su
terminal. Nunca comparta valores de credenciales. La fixture es idempotente.

En otra terminal:

```bash
cd frontend
npm ci
npm start
```

Abra http://localhost:4200; API y documentación local en http://localhost:8000/docs.
El proxy local reenvía /api/** a http://127.0.0.1:8000, retirando el prefijo /api.
Para compilar Angular: `npm run build` desde frontend/.

## Contratos obligatorios

| Ruta | Resultado esperado |
|---|---|
| GET /health | 200, {"status":"ok"}; señal de proceso vivo |
| GET /projects | 200, lista de proyectos; [] si no hay proyectos |
| GET /projects/{id}/summary | 200 con los indicadores definidos abajo |

Cada proyecto de la lista debe tener id (ObjectId serializado como cadena), name,
budget numérico y status. No exponga _id ni metadata interna. No se exige filtro
por status; el filtro heredado es opcional y no forma parte de la evaluación obligatoria.
Para summary: ID con formato inválido → 422; ID válido sin proyecto → 404.
Para una indisponibilidad de persistencia, devolver un error HTTP y no datos ficticios
con 200; no se exige un código específico ni pruebas exhaustivas de infraestructura.

Ejemplo de resumen SAT:

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

El resumen devuelve estos seis campos. completion_rate está entre 0 y 1 y vale cero
si no hay actividades. No mezcle actividades de proyectos diferentes.
Chatbots (64b000000000000000000002) no tiene actividades: sus cuatro indicadores
son cero. Se acepta tolerancia de 1e-6 para cálculos decimales.

## Dashboard obligatorio en Angular 21

Se proporciona un esqueleto compilable con HttpClient, tipos, selector y tarjetas.
La lista está conectada; el método summary y su consumo están pendientes.

- Cargue la lista desde la API y permita seleccionar un proyecto.
- Muestre nombre, actividades, completadas, horas totales y avance en porcentaje.
- Muestre estado de carga y mensaje visible ante fallos de lista o resumen.
- Presente ceros cuando no hay actividades; si la lista está vacía, indíquelo.
- Limpie indicadores anteriores al cambiar/deseleccionar proyecto o ante un error.
- Mantenga etiquetas accesibles y legibilidad en móvil y escritorio.

No se exige botón de reintento ni prueba de respuestas fuera de orden. Tampoco
login, CRUD visual, gráficas o una librería de UI. Los datos deben proceder de la
API y MongoDB reales; mocks son válidos únicamente en pruebas.

## Revisión técnica y pruebas

Identifique hasta tres problemas prioritarios del código o las pruebas heredadas.
Para cada uno indique ubicación, evidencia, consecuencia y solución. Corrija al menos
uno y verifique su corrección; puede ser parte de los cambios del flujo obligatorio.
No se exige refactorización independiente ni una arquitectura particular.

Verifique al menos tres casos de backend: resumen correcto, proyecto inexistente y
proyecto sin actividades. Las pruebas públicas ya los plantean: complételas o
fortalézcalas; no necesita duplicarlas. Mantenga también la prueba de ID inválido.
Añada una prueba automatizada útil de frontend que ejercite código productivo
(servicio HTTP o componente, por ejemplo resultado o error). Elija el runner y
registre el comando de ejecución. `review_examples/` contiene una prueba heredada
para inspección; no pertenece a la suite obligatoria.

## Despliegue

Publique Angular como Render Static Site y FastAPI como Render Web Service gratuito.
Use MongoDB Atlas Free para persistencia. No se exige Docker, dominio propio ni CI/CD
personalizado. No use una base real del laboratorio ni credenciales institucionales.

Referencias de configuración (confirme y adapte en su entrega):

| Servicio | Configuración de referencia |
|---|---|
| FastAPI | Raíz del repositorio; runtime Python 3.12; build: pip install -r requirements.txt |
| Arranque API | uvicorn app.main:app --host 0.0.0.0 --port $PORT |
| Angular | Root Directory: frontend; Node.js 24; build: npm ci && npm run build |
| Publicación Angular | dist/dashboard/browser, relativa a frontend |
| Variables backend | MONGO_URL, DATABASE y origen permitido del dashboard según su implementación |

El proxy de ng serve no se publica en el build: configure la URL HTTPS de la API
para el frontend desplegado o una ruta equivalente. Configure CORS para el origen
concreto del dashboard si usa dominios separados. Una URL pública de API no es un
secreto; credenciales de MongoDB y tokens privados nunca deben llegar al bundle Angular.
Configure usuario y acceso de red de Atlas y documente el procedimiento sin secretos.

Cargue la fixture desde su equipo con `python -m scripts.seed`, apuntando a Atlas
mediante variables de entorno. No se requiere shell remoto en Render. Confirme
persistencia y que dashboard y API consultan esa misma base. El servicio gratuito
puede suspenderse tras inactividad; no se evalúa la velocidad del primer arranque.
Si una restricción de cuenta o incidencia del proveedor bloquea el deploy, documente
evidencia y entregue una demostración local grabada para revisión del evaluador.

Referencias oficiales:
- https://render.com/docs/deploy-fastapi
- https://render.com/docs/static-sites
- https://render.com/docs/free
- https://www.mongodb.com/docs/atlas/tutorial/deploy-free-tier-cluster/

## Tareas y entrega

1. Ejecute y comprenda el repositorio.
2. Complete los dos endpoints obligatorios y sus pruebas.
3. Complete el dashboard Angular y una prueba automatizada de frontend.
4. Identifique hasta tres problemas prioritarios y corrija al menos uno.
5. Despliegue en Render, cargue Atlas y documente la verificación.

Entregue repositorio o ZIP y un único informe breve: DECISIONS.md. Incluya allí URLs
del dashboard y API, comandos de ejecución/build/pruebas, configuración sin secretos,
los tres hallazgos, corrección verificada, herramientas utilizadas y pendientes.
Adjunte una captura del dashboard con datos reales y evidencia de un estado de error.
No incluya node_modules, entornos virtuales ni credenciales. Se evalúan correctitud,
integración, criterio y reproducibilidad; no volumen de código ni decoración.

## Estructura

```text
app/               backend y código heredado para revisión
frontend/          dashboard Angular 21, servicio HTTP y proxy local
scripts/seed.py    datos ficticios idempotentes
tests/            suite obligatoria de backend
review_examples/   ejemplo de prueba heredada para inspección
DECISIONS.md       único informe de entrega
Dockerfile         material opcional de revisión
compose.yaml       material opcional de revisión
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
review_examples/test_legacy_mock.py
scripts/__init__.py
scripts/seed.py
tests/conftest.py
tests/test_api.py
```
