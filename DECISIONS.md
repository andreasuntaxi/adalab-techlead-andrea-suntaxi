# Informe de entrega

## URLs y ejecución



Dashboard Render:https://ada-dashboard-andrea-suntaxi.onrender.com/
API Render: https://adalab-techlead-andrea-suntaxi.onrender.com/
Repositorio: https://github.com/andreasuntaxi/adalab-techlead-andrea-suntaxi



Comandos locales, build y pruebas:
---


Desde la raíz del repositorio, en PowerShell:

    py -3.12 -m venv .venv

    .\.venv\Scripts\Activate.ps1

    python -m pip install -r requirements.txt

    python -m pytest -q



Antes de cargar los datos o iniciar la API, configurar MONGO_URL con la URI privada de Atlas y DATABASE con ada_exam en la misma sesión. La contraseña debe estar codificada para su uso en la URI. No incluir credenciales en el repositorio.



    $env:DATABASE = "ada_exam"

    python -m scripts.seed

    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000



Desde otra ventana, para el frontend:



    cd frontend

    npm ci

    npx ng test --watch=false

    npm run build

    npm start



La versión final del frontend consulta la API pública de Render. Su configuración CORS permite el origen del dashboard publicado. Para reproducir el funcionamiento completamente local, cambiar baseUrl a /api en projects.service.ts y su prueba, configurar DASHBOARD_ORIGIN como http://127.0.0.1:4200 y reiniciar la API. El servidor de desarrollo utiliza proxy.conf.json.



## Hasta tres problemas prioritarios

Ubicación, evidencia, consecuencia y solución. Señale al menos una corrección
realizada y cómo la verificó.



1. ###### Exposición de campos internos en el listado de proyectos.
* Ubicación: app/main.py, función list_projects; tests/test_api.py, test_list.
* Evidencia: el endpoint devolvía todos los campos del documento. Al incorporar metadata y created_by en la fixture de prueba, test_list falló porque ambos campos
* aparecían en la respuesta.
* Consecuencia: información interna podía incorporarse al contrato público de la API sin control.
* Solución realizada: construir una respuesta explícita con id, name, budget y status; convertir el identificador a texto y el presupuesto a número. El filtro por estado se aplica en la consulta a MongoDB.
* Verificación: test_list y test_empty_list pasaron. La suite completa terminó con 7 pruebas aprobadas.



###### 2. Configuración de base de datos y CORS no preparada para despliegue.



* Ubicación: app/config.py y configuración de CORSMiddleware en app/main.py.
* Evidencia: la configuración original fijaba MongoDB en localhost y permitía cualquier origen mediante allow_origins=["*"].
* Consecuencia: las variables del proveedor no configuraban la conexión a Atlas y la política CORS no delimitaba el dashboard autorizado.
* Solución realizada: leer MONGO_URL, DATABASE, REPORT_TOKEN y DASHBOARD_ORIGIN desde variables de entorno. Restringir CORS al origen configurado y al método GET utilizado por el dashboard.
* Verificación: carga del fixture en Atlas, consultas desde la API pública y visualización de SAT y Chatbots en el dashboard publicado. Las 7 pruebas backend siguieron aprobadas.



###### 3. Prueba heredada que no verifica el comportamiento real.



* Ubicación: review_examples/test_legacy_mock.py, test_repository_failure.
* Evidencia: configura un Mock para devolver {"status_code": 503} y comprueba ese mismo valor. No ejecuta un endpoint ni provoca un fallo real de persistencia.
* Consecuencia: puede aprobar aunque la aplicación gestione incorrectamente los errores de la base de datos.
* Solución propuesta: provocar una excepción en la dependencia de persistencia utilizada por el endpoint y comprobar, mediante TestClient, que se devuelve un error HTTP y no una respuesta exitosa con datos ficticios. El ejemplo heredado fue revisado y no se modificó.



## Despliegue y configuración

Servicios, versiones, comandos, nombres de variables (sin valores secretos),
conexión a Atlas, carga de fixture y pasos reproducibles.



###### Backend: 

Render Web Service, plan Free, runtime Python 3.12.10, región Ohio, rama master y directorio raíz del repositorio.



###### Comando de build:



    pip install -r requirements.txt



###### Comando de inicio:



    uvicorn app.main:app --host 0.0.0.0 --port $PORT



###### Variables del backend:



* PYTHON_VERSION: 3.12.10.
* MONGO_URL: URI privada de MongoDB Atlas.
* DATABASE: ada_exam.
* DASHBOARD_ORIGIN: https://ada-dashboard-andrea-suntaxi.onrender.com.
* REPORT_TOKEN: admitida por la configuración; no utilizada por el flujo del dashboard.
* PORT: proporcionada por Render.



###### Frontend: 

Render Static Site, rama master, Root Directory frontend y Node.js 24.15.0 mediante NODE_VERSION. Angular 21.0.0.



Comando de build:



    npm ci && npm run build



Publish Directory:



    dist/dashboard/browser



El servicio Angular utiliza la URL HTTPS de la API pública. El frontend no recibe credenciales de MongoDB.



###### Persistencia: 

MongoDB Atlas Free, clúster ada-cluster, proveedor AWS, región São Paulo y base ada_exam. Se utiliza el usuario de base de datos ada_app.



La lista de acceso de Atlas permite la IP del equipo utilizado para las pruebas y los rangos de salida de Render:



- 74.220.50.0/24.

- 74.220.58.0/24.



Pasos para reproducir el despliegue:



1. Clonar el repositorio e instalar las dependencias.

2. Crear el clúster y el usuario de base de datos en Atlas.

3. Autorizar las IP de los equipos o servicios que se conectarán.

4. Configurar MONGO_URL y DATABASE en la sesión local.

5. Ejecutar python -m scripts.seed; el resultado comprobado fue Fixture loaded.

6. Crear el Web Service con los comandos y variables indicados.

7. Autorizar en Atlas los rangos de salida correspondientes al servicio.

8. Crear el Static Site con la configuración indicada.

9. Configurar DASHBOARD_ORIGIN con el origen exacto del Static Site y volver a desplegar la API.

10. Verificar los endpoints y seleccionar ambos proyectos en el dashboard.



El fixture es idempotente: actualiza o crea los registros de ejemplo sin eliminar otros documentos. La API local y la desplegada consultaron la misma base de Atlas.







## Verificación

Resultado de pruebas backend y frontend; SAT y Chatbots en navegador con datos reales;
captura del dashboard y evidencia de manejo de error. Limitaciones observadas.



###### Backend:



- Resultado inicial: 2 pruebas aprobadas y 4 fallidas; el resumen respondía 501.

- Resultado final: 7 pruebas aprobadas.

- Casos cubiertos: health, contrato del listado, listado vacío, resumen de SAT, separación de actividades entre proyectos, proyecto inexistente, proyecto sin actividades e identificador inválido.

- Se mantiene una advertencia de deprecación de Starlette relacionada con BlockingPortal; no impidió la ejecución.



###### Frontend:



- 1 prueba automatizada aprobada con Vitest.

- La prueba ejecuta ProjectsService, verifica la petición GET del resumen y comprueba los indicadores devueltos.

- npm run build terminó correctamente tanto localmente como en Render.



###### Verificación con datos reales de Atlas:



- /health devolvió {"status":"ok"}. Este endpoint verifica que la aplicación está activa; no comprueba la conexión a MongoDB.

- /projects devolvió SAT y Chatbots con los cuatro campos previstos.

- SAT: 3 actividades, 2 completadas, 35 horas y completion_rate de 2/3.

- Chatbots: 0 actividades, 0 completadas, 0 horas y avance 0.

- Se comprobaron ambos proyectos en el dashboard público.



###### Verificación manual del dashboard:



- Estados de carga, resultado, selección vacía y error.

- Limpieza de los indicadores al cambiar o quitar la selección.

- Al detener la API local, la consulta mostró el mensaje de error y ocultó los indicadores anteriores.

- La carga inicial sin API mostró un error de listado.

- Revisión visual en escritorio y en una vista de 375 × 812 píxeles.



###### Evidencias:



* [SAT publicado en Render](evidence/dashboard-render-sat.png).
* [Chatbots publicado en Render](evidence/dashboard-render-chatbots.png).
* [Error de consulta del resumen en entorno local](evidence/dashboard-error-resumen.png).
* [SAT en entorno local](evidence/dashboard-sat.png).
* [Chatbots en entorno local](evidence/dashboard-chatbots.png).



La prueba automatizada frontend cubre el servicio HTTP. Los estados del componente y la presentación se verificaron manualmente. La evidencia de error corresponde al entorno local.





## Herramientas y pendientes

Herramientas usadas y cómo verificó una modificación asistida por IA (o propia si
no utilizó IA). Trabajo no completado. Incidencias del proveedor con evidencia, si aplica.



Herramientas utilizadas: PowerShell, Git, GitHub, Python, pytest, mongomock, FastAPI, PyMongo, MongoDB Atlas, Node.js, npm, Angular, Vitest, Render y herramientas de desarrollo del navegador.



Se utilizó ChatGPT/Codex como apoyo para guiar la configuración. Las modificaciones asistidas se verificaron mediante lectura de los archivos guardados, pruebas automatizadas, compilación y consultas con datos reales. Por ejemplo, la corrección del listado se comprobó con una prueba que primero falló al detectar campos internos y después pasó con la respuesta explícita.



El análisis npm audit informó 20 vulnerabilidades en el árbol de dependencias: 1 baja, 5 moderadas, 13 altas y 1 crítica. No se aplicó npm audit fix --force. Se requiere revisar las dependencias afectadas, actualizar de forma compatible y repetir las pruebas y el build.



La prueba heredada de review_examples se analizó, pero su sustitución por una prueba del manejo real de errores no se realizó.



Durante la configuración de Atlas se produjo un error de autenticación. Se corrigieron las credenciales y se confirmó la solución con Fixture loaded y las consultas posteriores. No se identificó una incidencia del proveedor que impidiera completar el despliegue.


