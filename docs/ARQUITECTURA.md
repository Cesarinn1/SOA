# Arquitectura Unificada de Servicios - Universidad Autonoma Veracruzana

## 1. Vision General

Este documento describe la arquitectura unificada basada en servicios (SOA) para integrar los diferentes sistemas academicos de la Universidad Autonoma Veracruzana.

## 2. Problematica Actual

La universidad cuenta con sistemas desarrollados de forma independiente:

| Sistema | Tecnologia | Estado |
|---------|-----------|--------|
| Sistema de Matriculas | SOAP (parcial) | 5 anos |
| Plataforma de Cursos Online | REST API | Moderno pero aislado |
| Sistema de Calificaciones | BD independiente | API parcial |
| Aplicacion Movil | Desarrollo reciente | Sin integracion |

## 3. Arquitectura Propuesta

### 3.1 Diagrama de Arquitectura

```
                    +----------------------------------+
                    |        FRONTEND UNIFICADO        |
                    |   (Web App / Mobile App)         |
                    +----------------+-----------------+
                                     |
                                     v
                    +----------------------------------+
                    |         API GATEWAY              |
                    |   (Punto de entrada unico)       |
                    +----------------+-----------------+
                                     |
            +------------------------+------------------------+
            |                        |                        |
            v                        v                        v
+-------------------+    +-------------------+    +-------------------+
|   SERVICIO SOAP   |    |   SERVICIO REST   |    |   SERVICIO REST   |
|   (Estudiantes/   |    |     (Cursos)      |    |  (Calificaciones) |
|    Matriculas)    |    |                   |    |                   |
|   Python + Zeep   |    | Java Spring Boot  |    |    Node.js (*)    |
+--------+----------+    +--------+----------+    +--------+----------+
         |                        |                        |
         v                        v                        v
+-------------------+    +-------------------+    +-------------------+
|      MySQL        |    |      MySQL        |    |   PostgreSQL (*)  |
|     (Local)       |    |      (Web)        |    |      (Web)        |
+-------------------+    +-------------------+    +-------------------+

(*) Fase futura
```

### 3.2 Componentes Principales

#### 3.2.1 API SOAP - Sistema de Estudiantes/Matriculas (Python)
- **Tecnologia**: Python + Spyne + MySQL
- **Protocolo**: SOAP/XML
- **Puerto**: 8000
- **Funcionalidad**: CRUD de estudiantes, consulta de matriculas

**Operaciones SOAP disponibles:**
- `obtener_estudiante(matricula)` - Obtiene informacion de un estudiante
- `listar_estudiantes()` - Lista todos los estudiantes
- `crear_estudiante(datos)` - Registra un nuevo estudiante
- `actualizar_estudiante(matricula, datos)` - Actualiza datos del estudiante
- `eliminar_estudiante(matricula)` - Elimina un estudiante

#### 3.2.2 API REST - Sistema de Cursos (Java Spring Boot)
- **Tecnologia**: Java 17 + Spring Boot + MySQL
- **Protocolo**: REST/JSON
- **Puerto**: 8080
- **Funcionalidad**: CRUD de cursos, gestion de grupos

**Endpoints REST disponibles:**

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | `/api/cursos` | Listar todos los cursos |
| GET | `/api/cursos/{id}` | Obtener curso por ID |
| GET | `/api/cursos/codigo/{codigo}` | Obtener curso por codigo |
| POST | `/api/cursos` | Crear nuevo curso |
| PUT | `/api/cursos/{id}` | Actualizar curso |
| DELETE | `/api/cursos/{id}` | Eliminar curso |

### 3.3 Interoperabilidad SOAP/REST

```
+------------------+                      +------------------+
|   Cliente REST   |                      |   Cliente SOAP   |
|   (JSON)         |                      |   (XML)          |
+--------+---------+                      +--------+---------+
         |                                         |
         v                                         v
+------------------+                      +------------------+
|   API Gateway    |<-------------------->|   API Gateway    |
|   Traduccion     |   Transformacion     |   Traduccion     |
|   JSON <-> XML   |   de mensajes        |   XML <-> JSON   |
+--------+---------+                      +--------+---------+
         |                                         |
         v                                         v
+------------------+                      +------------------+
|  Servicio REST   |                      |  Servicio SOAP   |
|  (Cursos)        |                      |  (Estudiantes)   |
+------------------+                      +------------------+
```

## 4. Modelo de Datos

### 4.1 Entidades Principales

```
+---------------+       +---------------+       +---------------+
|  FACULTADES   |       |   CARRERAS    |       |    CURSOS     |
+---------------+       +---------------+       +---------------+
| id_facultad   |<----->| id_carrera    |<----->| id_curso      |
| nombre        |       | id_facultad   |       | codigo        |
| codigo        |       | nombre        |       | nombre        |
| descripcion   |       | codigo        |       | creditos      |
+---------------+       | duracion      |       | id_carrera    |
                        +---------------+       +---------------+
                               ^
                               |
+---------------+       +---------------+       +---------------+
| ESTUDIANTES   |       | INSCRIPCIONES |       |    GRUPOS     |
+---------------+       +---------------+       +---------------+
| id_estudiante |<----->| id_inscripcion|       | id_grupo      |
| matricula     |       | id_estudiante |       | id_curso      |
| nombre        |       | id_carrera    |       | id_profesor   |
| email         |       | semestre      |       | periodo       |
| estatus       |       +---------------+       | horario       |
+---------------+                               +---------------+
                                                       ^
                                                       |
+---------------+                               +---------------+
|  PROFESORES   |------------------------------>| CALIFICACIONES|
+---------------+                               +---------------+
| id_profesor   |                               | id_estudiante |
| nombre        |                               | id_grupo      |
| email         |                               | calificacion  |
| especialidad  |                               | estatus       |
+---------------+                               +---------------+
```

## 5. Flujo de Comunicacion

### 5.1 Ejemplo: Consulta de Estudiante con sus Cursos

```
1. Cliente -> API Gateway: GET /estudiante/S21001234/cursos

2. API Gateway -> Servicio SOAP (Estudiantes):
   <soap:Envelope>
     <soap:Body>
       <obtener_estudiante>
         <matricula>S21001234</matricula>
       </obtener_estudiante>
     </soap:Body>
   </soap:Envelope>

3. Servicio SOAP -> API Gateway: Respuesta XML con datos del estudiante

4. API Gateway -> Servicio REST (Cursos):
   GET /api/cursos/estudiante/1

5. Servicio REST -> API Gateway: Respuesta JSON con cursos

6. API Gateway: Combina respuestas y transforma a formato solicitado

7. API Gateway -> Cliente: Respuesta unificada JSON
```

## 6. Tecnologias Utilizadas

| Componente | Tecnologia | Version |
|------------|------------|---------|
| API SOAP | Python + Spyne | 3.11 |
| API REST | Java + Spring Boot | 17 / 3.x |
| Base de Datos | MySQL | 8.0 |
| Contenedores | Docker | 24.x |
| Documentacion API | Swagger/OpenAPI | 3.0 |
| Testing | Postman | Latest |

## 7. Seguridad (Fase Futura)

- Autenticacion JWT para APIs REST
- WS-Security para servicios SOAP
- HTTPS obligatorio
- Rate limiting en API Gateway
- Validacion de entrada en todos los endpoints

## 8. Escalabilidad

La arquitectura permite:
- Escalar servicios de forma independiente
- Agregar nuevos microservicios sin afectar los existentes
- Balanceo de carga por servicio
- Cache distribuido para consultas frecuentes

## 9. Estructura del Proyecto

```
uav-soa-project/
|-- api-soap-python/          # API SOAP en Python
|   |-- app.py                # Aplicacion principal
|   |-- requirements.txt      # Dependencias
|   |-- Dockerfile
|
|-- api-rest-java/            # API REST en Java
|   |-- src/
|   |   |-- main/
|   |       |-- java/com/uav/cursos/
|   |       |-- resources/
|   |-- pom.xml
|   |-- Dockerfile
|
|-- database/
|   |-- schema.sql            # Script de creacion de BD
|
|-- docs/
|   |-- ARQUITECTURA.md       # Este documento
|
|-- postman/
|   |-- UAV_SOA_Collection.json
|
|-- docker-compose.yml        # Orquestacion de servicios
|-- README.md
```

## 10. Autores

- Universidad Autonoma Veracruzana
- Materia: Arquitectura Orientada a Servicios
- Fecha: Noviembre 2025
