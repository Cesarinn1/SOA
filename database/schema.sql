-- ============================================
-- UNIVERSIDAD AUTONOMA VERACRUZANA
-- Sistema Unificado de Servicios Academicos
-- Modelado de Base de Datos
-- ============================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS uav_sistema_academico;
USE uav_sistema_academico;

-- ============================================
-- MODULO: ESTUDIANTES (Sistema de Matriculas - SOAP)
-- ============================================

CREATE TABLE IF NOT EXISTS estudiantes (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE,
    direccion TEXT,
    fecha_ingreso DATE NOT NULL,
    estatus ENUM('activo', 'inactivo', 'egresado', 'baja') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================
-- MODULO: CARRERAS Y FACULTADES
-- ============================================

CREATE TABLE IF NOT EXISTS facultades (
    id_facultad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS carreras (
    id_carrera INT AUTO_INCREMENT PRIMARY KEY,
    id_facultad INT NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    duracion_semestres INT DEFAULT 8,
    modalidad ENUM('presencial', 'virtual', 'mixta') DEFAULT 'presencial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_facultad) REFERENCES facultades(id_facultad)
);

-- ============================================
-- MODULO: CURSOS (Plataforma de Cursos - REST)
-- ============================================

CREATE TABLE IF NOT EXISTS cursos (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    descripcion TEXT,
    creditos INT NOT NULL,
    horas_teoricas INT DEFAULT 0,
    horas_practicas INT DEFAULT 0,
    id_carrera INT,
    semestre INT,
    estatus ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- ============================================
-- MODULO: PROFESORES
-- ============================================

CREATE TABLE IF NOT EXISTS profesores (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    numero_empleado VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100),
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad VARCHAR(100),
    grado_academico ENUM('licenciatura', 'maestria', 'doctorado') DEFAULT 'licenciatura',
    id_facultad INT,
    estatus ENUM('activo', 'inactivo') DEFAULT 'activo',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_facultad) REFERENCES facultades(id_facultad)
);

-- ============================================
-- MODULO: INSCRIPCIONES (Matriculas)
-- ============================================

CREATE TABLE IF NOT EXISTS inscripciones (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_carrera INT NOT NULL,
    semestre_actual INT DEFAULT 1,
    fecha_inscripcion DATE NOT NULL,
    estatus ENUM('activa', 'suspendida', 'finalizada') DEFAULT 'activa',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_carrera) REFERENCES carreras(id_carrera)
);

-- ============================================
-- MODULO: GRUPOS Y HORARIOS
-- ============================================

CREATE TABLE IF NOT EXISTS grupos (
    id_grupo INT AUTO_INCREMENT PRIMARY KEY,
    id_curso INT NOT NULL,
    id_profesor INT NOT NULL,
    periodo VARCHAR(20) NOT NULL, -- Ej: "2025-1", "2025-2"
    cupo_maximo INT DEFAULT 30,
    cupo_actual INT DEFAULT 0,
    aula VARCHAR(20),
    horario VARCHAR(100),
    estatus ENUM('abierto', 'cerrado', 'cancelado') DEFAULT 'abierto',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_curso) REFERENCES cursos(id_curso),
    FOREIGN KEY (id_profesor) REFERENCES profesores(id_profesor)
);

-- ============================================
-- MODULO: CALIFICACIONES
-- ============================================

CREATE TABLE IF NOT EXISTS calificaciones (
    id_calificacion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_grupo INT NOT NULL,
    calificacion_parcial1 DECIMAL(4,2),
    calificacion_parcial2 DECIMAL(4,2),
    calificacion_parcial3 DECIMAL(4,2),
    calificacion_final DECIMAL(4,2),
    estatus ENUM('cursando', 'aprobado', 'reprobado', 'sin_derecho') DEFAULT 'cursando',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_estudiante) REFERENCES estudiantes(id_estudiante),
    FOREIGN KEY (id_grupo) REFERENCES grupos(id_grupo),
    UNIQUE KEY unique_estudiante_grupo (id_estudiante, id_grupo)
);

-- ============================================
-- DATOS DE PRUEBA
-- ============================================

-- Facultades
INSERT INTO facultades (nombre, codigo, descripcion) VALUES
('Facultad de Ingenieria', 'FI', 'Facultad de Ciencias de la Ingenieria'),
('Facultad de Ciencias Administrativas', 'FCA', 'Facultad de Administracion y Contaduria'),
('Facultad de Ciencias', 'FC', 'Facultad de Ciencias Exactas');

-- Carreras
INSERT INTO carreras (id_facultad, nombre, codigo, duracion_semestres, modalidad) VALUES
(1, 'Ingenieria en Sistemas Computacionales', 'ISC', 9, 'presencial'),
(1, 'Ingenieria en Software', 'ISW', 9, 'presencial'),
(2, 'Licenciatura en Administracion', 'LAE', 8, 'mixta'),
(3, 'Licenciatura en Matematicas', 'LMAT', 8, 'presencial');

-- Estudiantes
INSERT INTO estudiantes (matricula, nombre, apellido_paterno, apellido_materno, email, telefono, fecha_nacimiento, fecha_ingreso, estatus) VALUES
('S21001234', 'Juan Carlos', 'Garcia', 'Lopez', 'juan.garcia@estudiantes.uav.mx', '2281234567', '2000-05-15', '2021-08-01', 'activo'),
('S21001235', 'Maria Fernanda', 'Martinez', 'Hernandez', 'maria.martinez@estudiantes.uav.mx', '2281234568', '2001-03-22', '2021-08-01', 'activo'),
('S20001100', 'Pedro', 'Sanchez', 'Ruiz', 'pedro.sanchez@estudiantes.uav.mx', '2281234569', '1999-11-10', '2020-08-01', 'activo'),
('S22001500', 'Ana Laura', 'Rodriguez', 'Perez', 'ana.rodriguez@estudiantes.uav.mx', '2281234570', '2002-07-08', '2022-08-01', 'activo'),
('S19000800', 'Roberto', 'Jimenez', 'Castro', 'roberto.jimenez@estudiantes.uav.mx', '2281234571', '1998-12-25', '2019-08-01', 'egresado');

-- Profesores
INSERT INTO profesores (numero_empleado, nombre, apellido_paterno, apellido_materno, email, especialidad, grado_academico, id_facultad) VALUES
('P10001', 'Carlos Alberto', 'Mendez', 'Vargas', 'carlos.mendez@uav.mx', 'Desarrollo de Software', 'maestria', 1),
('P10002', 'Laura Patricia', 'Gonzalez', 'Diaz', 'laura.gonzalez@uav.mx', 'Bases de Datos', 'doctorado', 1),
('P10003', 'Miguel Angel', 'Torres', 'Luna', 'miguel.torres@uav.mx', 'Redes y Telecomunicaciones', 'maestria', 1);

-- Cursos
INSERT INTO cursos (codigo, nombre, descripcion, creditos, horas_teoricas, horas_practicas, id_carrera, semestre) VALUES
('ISC101', 'Programacion I', 'Fundamentos de programacion y algoritmos', 8, 3, 2, 1, 1),
('ISC102', 'Matematicas Discretas', 'Logica y estructuras discretas', 6, 4, 0, 1, 1),
('ISC201', 'Estructura de Datos', 'Estructuras de datos y algoritmos avanzados', 8, 3, 2, 1, 2),
('ISC301', 'Bases de Datos', 'Diseno y administracion de bases de datos', 8, 3, 2, 1, 3),
('ISC401', 'Arquitectura de Software', 'Patrones y arquitecturas de software', 6, 3, 1, 1, 4),
('ISC501', 'Servicios Web', 'Desarrollo de servicios web SOAP y REST', 8, 2, 3, 1, 5);

-- Grupos
INSERT INTO grupos (id_curso, id_profesor, periodo, cupo_maximo, aula, horario) VALUES
(1, 1, '2025-1', 30, 'A101', 'Lunes y Miercoles 8:00-10:00'),
(2, 2, '2025-1', 35, 'A102', 'Martes y Jueves 10:00-12:00'),
(3, 1, '2025-1', 30, 'A103', 'Lunes y Miercoles 10:00-12:00'),
(4, 2, '2025-1', 25, 'LAB01', 'Viernes 8:00-12:00');

-- Inscripciones
INSERT INTO inscripciones (id_estudiante, id_carrera, semestre_actual, fecha_inscripcion) VALUES
(1, 1, 5, '2021-08-01'),
(2, 1, 5, '2021-08-01'),
(3, 1, 7, '2020-08-01'),
(4, 2, 3, '2022-08-01');

-- Calificaciones
INSERT INTO calificaciones (id_estudiante, id_grupo, calificacion_parcial1, calificacion_parcial2, calificacion_parcial3, calificacion_final, estatus) VALUES
(1, 1, 85.50, 90.00, 88.00, 88.00, 'aprobado'),
(1, 2, 78.00, 82.00, 80.00, 80.00, 'aprobado'),
(2, 1, 92.00, 95.00, 93.00, 93.00, 'aprobado'),
(3, 3, 70.00, 75.00, NULL, NULL, 'cursando');
