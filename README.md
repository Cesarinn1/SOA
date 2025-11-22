# Sistema Academico UAV - Arquitectura Orientada a Servicios

## Universidad Autonoma Veracruzana
### Materia: Arquitectura Orientada a Servicios
### Fecha: Noviembre 2025

---

## Descripcion del Proyecto

Este proyecto implementa la primera fase de una plataforma web unificada de servicios academicos que integra diferentes sistemas mediante una Arquitectura Orientada a Servicios (SOA).

### Problematica
La Universidad Autonoma Veracruzana enfrenta una crisis de integracion tecnologica entre sus sistemas:
- Sistema de Matriculas (SOAP parcial - 5 anos)
- Plataforma de Cursos Online (REST moderna pero aislada)
- Sistema de Calificaciones (BD independiente con API parcial)
- Aplicacion Movil (sin integracion completa)

### Solucion
Arquitectura unificada que integra:
- Servicios SOAP y APIs RESTful
- Interoperabilidad entre formatos XML y JSON
- Arquitectura escalable basada en microservicios

---

## Estructura del Proyecto

```
uav-soa-project/
|-- api-soap-python/          # API SOAP - Estudiantes (Python)
|   |-- app.py                # Aplicacion principal
|   |-- requirements.txt      # Dependencias Python
|   |-- Dockerfile
|
|-- api-rest-java/            # API REST - Cursos (Java Spring Boot)
|   |-- src/
|   |   |-- main/
|   |       |-- java/com/uav/cursos/
|   |       |-- resources/application.properties
|   |-- pom.xml
|   |-- Dockerfile
|
|-- database/
|   |-- schema.sql            # Script de creacion de BD
|
|-- docs/
|   |-- ARQUITECTURA.md       # Documento de arquitectura
|
|-- postman/
|   |-- UAV_SOA_Collection.json  # Coleccion de pruebas
|
|-- docker-compose.yml        # Orquestacion de servicios
|-- README.md                 # Este archivo
```

---

## Tecnologias Utilizadas

| Componente | Tecnologia | Version |
|------------|------------|---------|
| API SOAP | Python + Spyne | 3.11 |
| API REST | Java + Spring Boot | 17 / 3.2 |
| Base de Datos | MySQL | 8.0 |
| Contenedores | Docker | 24.x |
| Testing | Postman | Latest |

---

## Requisitos Previos

### Opcion 1: Ejecucion con Docker (Recomendado)
- Docker Desktop instalado
- Docker Compose

### Opcion 2: Ejecucion Local
- Python 3.11+
- Java 17+
- Maven 3.9+
- MySQL 8.0+

---

## Instalacion y Ejecucion

### Opcion 1: Con Docker Compose

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/uav-soa-project.git
cd uav-soa-project

# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Opcion 2: Ejecucion Local

#### 1. Configurar Base de Datos MySQL

```bash
# Conectar a MySQL
mysql -u root -p

# Ejecutar el script de creacion
source database/schema.sql
```

#### 2. Iniciar API SOAP (Python)

```bash
cd api-soap-python

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
python app.py
```

El servidor SOAP estara disponible en: `http://localhost:8000`
WSDL: `http://localhost:8000/?wsdl`

#### 3. Iniciar API REST (Java)

```bash
cd api-rest-java

# Compilar y ejecutar con Maven
mvn spring-boot:run
```

El servidor REST estara disponible en: `http://localhost:8080`
Swagger UI: `http://localhost:8080/swagger-ui.html`

---

## Endpoints Disponibles

### API REST - Cursos (Java)

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/cursos` | Listar todos los cursos |
| GET | `/api/cursos/{id}` | Obtener curso por ID |
| GET | `/api/cursos/codigo/{codigo}` | Obtener curso por codigo |
| POST | `/api/cursos` | Crear nuevo curso |
| PUT | `/api/cursos/{id}` | Actualizar curso |
| DELETE | `/api/cursos/{id}` | Eliminar curso |
| GET | `/api/cursos/carrera/{id}` | Cursos por carrera |
| GET | `/api/cursos/semestre/{num}` | Cursos por semestre |
| GET | `/api/cursos/activos` | Solo cursos activos |
| GET | `/api/cursos/buscar?nombre=x` | Buscar por nombre |

### API SOAP - Estudiantes (Python)

| Operacion | Descripcion |
|-----------|-------------|
| `obtener_estudiante(matricula)` | Obtener estudiante por matricula |
| `listar_estudiantes()` | Listar todos los estudiantes |
| `crear_estudiante(...)` | Crear nuevo estudiante |
| `actualizar_estudiante(...)` | Actualizar estudiante |
| `eliminar_estudiante(matricula)` | Eliminar estudiante |
| `buscar_estudiantes_por_estatus(estatus)` | Filtrar por estatus |

---

## Pruebas con Postman

1. Importar la coleccion desde `postman/UAV_SOA_Collection.json`
2. La coleccion incluye pruebas para ambas APIs
3. Asegurate de que los servicios esten corriendo antes de ejecutar las pruebas

### Ejemplos de Peticiones

#### REST - Crear Curso
```bash
curl -X POST http://localhost:8080/api/cursos \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "ISC601",
    "nombre": "Inteligencia Artificial",
    "descripcion": "Fundamentos de IA",
    "creditos": 8,
    "horasTeoricas": 3,
    "horasPracticas": 2,
    "idCarrera": 1,
    "semestre": 6,
    "estatus": "activo"
  }'
```

#### SOAP - Obtener Estudiante
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: text/xml" \
  -d '<?xml version="1.0"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="http://uav.mx/servicios/estudiantes">
  <soap:Body>
    <tns:obtener_estudiante>
      <tns:matricula>S21001234</tns:matricula>
    </tns:obtener_estudiante>
  </soap:Body>
</soap:Envelope>'
```

---

## Modelo de Base de Datos

El sistema incluye las siguientes entidades:

- **Estudiantes**: Informacion de alumnos matriculados
- **Profesores**: Datos del personal docente
- **Facultades**: Divisiones academicas
- **Carreras**: Programas academicos
- **Cursos**: Materias disponibles
- **Grupos**: Instancias de cursos por periodo
- **Inscripciones**: Relacion estudiante-carrera
- **Calificaciones**: Evaluaciones de estudiantes

Ver diagrama completo en `docs/ARQUITECTURA.md`

---

## Entregables

1. **Analisis y Diseno**: `database/schema.sql` - Modelado de BD
2. **Arquitectura**: `docs/ARQUITECTURA.md` - Diseno SOAP/REST
3. **API SOAP**: `api-soap-python/` - Python + MySQL
4. **API REST**: `api-rest-java/` - Java Spring Boot + MySQL
5. **Pruebas**: `postman/UAV_SOA_Collection.json`
6. **Repositorio**: Este repositorio de GitHub

---

## Autor

- **Nombre**: Cesar Guadarrama
- **Universidad**: Universidad Autonoma Veracruzana
- **Materia**: Arquitectura Orientada a Servicios
- **Fecha**: Noviembre 2025

---

## Licencia

Este proyecto es de uso academico para la materia de Arquitectura Orientada a Servicios.
