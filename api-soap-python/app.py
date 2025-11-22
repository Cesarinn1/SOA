"""
API SOAP - Sistema de Estudiantes/Matriculas
Universidad Autonoma Veracruzana
Arquitectura Orientada a Servicios

Este servicio implementa operaciones CRUD para la entidad Estudiantes
utilizando el protocolo SOAP con Python y Spyne.
"""

from spyne import Application, Service, rpc, Unicode, Integer, Array, ComplexModel, Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
import mysql.connector
from mysql.connector import Error
import logging

# Configuracion de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuracion de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'uav_sistema_academico',
    'user': 'root',
    'password': ''  # Cambiar segun tu configuracion
}


def get_db_connection():
    """Establece conexion con la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        logger.error(f"Error conectando a MySQL: {e}")
        return None


class Estudiante(ComplexModel):
    """Modelo complejo para representar un Estudiante en SOAP"""
    id_estudiante = Integer
    matricula = Unicode
    nombre = Unicode
    apellido_paterno = Unicode
    apellido_materno = Unicode
    email = Unicode
    telefono = Unicode
    fecha_nacimiento = Unicode
    direccion = Unicode
    fecha_ingreso = Unicode
    estatus = Unicode


class EstudianteInput(ComplexModel):
    """Modelo para entrada de datos de estudiante"""
    matricula = Unicode
    nombre = Unicode
    apellido_paterno = Unicode
    apellido_materno = Unicode
    email = Unicode
    telefono = Unicode
    fecha_nacimiento = Unicode
    direccion = Unicode
    fecha_ingreso = Unicode
    estatus = Unicode


class RespuestaOperacion(ComplexModel):
    """Modelo para respuestas de operaciones"""
    exito = Unicode
    mensaje = Unicode
    codigo = Integer


class EstudianteService(Service):
    """
    Servicio SOAP para gestion de Estudiantes

    Operaciones disponibles:
    - obtener_estudiante: Obtiene un estudiante por matricula
    - listar_estudiantes: Lista todos los estudiantes
    - crear_estudiante: Crea un nuevo estudiante
    - actualizar_estudiante: Actualiza datos de un estudiante
    - eliminar_estudiante: Elimina un estudiante
    """

    @rpc(Unicode, _returns=Estudiante)
    def obtener_estudiante(ctx, matricula):
        """
        Obtiene la informacion de un estudiante por su matricula

        Args:
            matricula: Matricula del estudiante (ej: S21001234)

        Returns:
            Estudiante: Objeto con los datos del estudiante
        """
        logger.info(f"Consultando estudiante con matricula: {matricula}")

        connection = get_db_connection()
        if not connection:
            return None

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_estudiante, matricula, nombre, apellido_paterno,
                       apellido_materno, email, telefono,
                       DATE_FORMAT(fecha_nacimiento, '%Y-%m-%d') as fecha_nacimiento,
                       direccion,
                       DATE_FORMAT(fecha_ingreso, '%Y-%m-%d') as fecha_ingreso,
                       estatus
                FROM estudiantes
                WHERE matricula = %s
            """
            cursor.execute(query, (matricula,))
            result = cursor.fetchone()

            if result:
                estudiante = Estudiante(
                    id_estudiante=result['id_estudiante'],
                    matricula=result['matricula'],
                    nombre=result['nombre'],
                    apellido_paterno=result['apellido_paterno'],
                    apellido_materno=result['apellido_materno'] or '',
                    email=result['email'],
                    telefono=result['telefono'] or '',
                    fecha_nacimiento=result['fecha_nacimiento'] or '',
                    direccion=result['direccion'] or '',
                    fecha_ingreso=result['fecha_ingreso'],
                    estatus=result['estatus']
                )
                logger.info(f"Estudiante encontrado: {result['nombre']}")
                return estudiante
            else:
                logger.warning(f"Estudiante no encontrado: {matricula}")
                return None

        except Error as e:
            logger.error(f"Error en consulta: {e}")
            return None
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @rpc(_returns=Iterable(Estudiante))
    def listar_estudiantes(ctx):
        """
        Lista todos los estudiantes registrados en el sistema

        Returns:
            Iterable[Estudiante]: Lista de estudiantes
        """
        logger.info("Listando todos los estudiantes")

        connection = get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_estudiante, matricula, nombre, apellido_paterno,
                       apellido_materno, email, telefono,
                       DATE_FORMAT(fecha_nacimiento, '%Y-%m-%d') as fecha_nacimiento,
                       direccion,
                       DATE_FORMAT(fecha_ingreso, '%Y-%m-%d') as fecha_ingreso,
                       estatus
                FROM estudiantes
                ORDER BY apellido_paterno, apellido_materno, nombre
            """
            cursor.execute(query)
            results = cursor.fetchall()

            estudiantes = []
            for result in results:
                estudiante = Estudiante(
                    id_estudiante=result['id_estudiante'],
                    matricula=result['matricula'],
                    nombre=result['nombre'],
                    apellido_paterno=result['apellido_paterno'],
                    apellido_materno=result['apellido_materno'] or '',
                    email=result['email'],
                    telefono=result['telefono'] or '',
                    fecha_nacimiento=result['fecha_nacimiento'] or '',
                    direccion=result['direccion'] or '',
                    fecha_ingreso=result['fecha_ingreso'],
                    estatus=result['estatus']
                )
                estudiantes.append(estudiante)

            logger.info(f"Total de estudiantes encontrados: {len(estudiantes)}")
            return estudiantes

        except Error as e:
            logger.error(f"Error listando estudiantes: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,
         _returns=RespuestaOperacion)
    def crear_estudiante(ctx, matricula, nombre, apellido_paterno, apellido_materno,
                         email, telefono, fecha_nacimiento, direccion, fecha_ingreso):
        """
        Crea un nuevo estudiante en el sistema

        Args:
            matricula: Matricula unica del estudiante
            nombre: Nombre(s) del estudiante
            apellido_paterno: Apellido paterno
            apellido_materno: Apellido materno
            email: Correo electronico institucional
            telefono: Numero de telefono
            fecha_nacimiento: Fecha de nacimiento (YYYY-MM-DD)
            direccion: Direccion del estudiante
            fecha_ingreso: Fecha de ingreso a la universidad (YYYY-MM-DD)

        Returns:
            RespuestaOperacion: Resultado de la operacion
        """
        logger.info(f"Creando nuevo estudiante: {matricula}")

        connection = get_db_connection()
        if not connection:
            return RespuestaOperacion(
                exito='false',
                mensaje='Error de conexion a la base de datos',
                codigo=500
            )

        try:
            cursor = connection.cursor()
            query = """
                INSERT INTO estudiantes
                (matricula, nombre, apellido_paterno, apellido_materno,
                 email, telefono, fecha_nacimiento, direccion, fecha_ingreso, estatus)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'activo')
            """
            cursor.execute(query, (
                matricula, nombre, apellido_paterno, apellido_materno,
                email, telefono, fecha_nacimiento or None, direccion, fecha_ingreso
            ))
            connection.commit()

            logger.info(f"Estudiante creado exitosamente: {matricula}")
            return RespuestaOperacion(
                exito='true',
                mensaje=f'Estudiante {matricula} creado exitosamente',
                codigo=201
            )

        except Error as e:
            logger.error(f"Error creando estudiante: {e}")
            return RespuestaOperacion(
                exito='false',
                mensaje=f'Error al crear estudiante: {str(e)}',
                codigo=400
            )
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @rpc(Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode,
         _returns=RespuestaOperacion)
    def actualizar_estudiante(ctx, matricula, nombre, apellido_paterno, apellido_materno,
                              email, telefono, fecha_nacimiento, direccion, fecha_ingreso, estatus):
        """
        Actualiza los datos de un estudiante existente

        Args:
            matricula: Matricula del estudiante a actualizar
            nombre: Nuevo nombre
            apellido_paterno: Nuevo apellido paterno
            apellido_materno: Nuevo apellido materno
            email: Nuevo email
            telefono: Nuevo telefono
            fecha_nacimiento: Nueva fecha de nacimiento
            direccion: Nueva direccion
            fecha_ingreso: Nueva fecha de ingreso
            estatus: Nuevo estatus (activo, inactivo, egresado, baja)

        Returns:
            RespuestaOperacion: Resultado de la operacion
        """
        logger.info(f"Actualizando estudiante: {matricula}")

        connection = get_db_connection()
        if not connection:
            return RespuestaOperacion(
                exito='false',
                mensaje='Error de conexion a la base de datos',
                codigo=500
            )

        try:
            cursor = connection.cursor()
            query = """
                UPDATE estudiantes
                SET nombre = %s, apellido_paterno = %s, apellido_materno = %s,
                    email = %s, telefono = %s, fecha_nacimiento = %s,
                    direccion = %s, fecha_ingreso = %s, estatus = %s
                WHERE matricula = %s
            """
            cursor.execute(query, (
                nombre, apellido_paterno, apellido_materno, email, telefono,
                fecha_nacimiento or None, direccion, fecha_ingreso, estatus, matricula
            ))
            connection.commit()

            if cursor.rowcount > 0:
                logger.info(f"Estudiante actualizado: {matricula}")
                return RespuestaOperacion(
                    exito='true',
                    mensaje=f'Estudiante {matricula} actualizado exitosamente',
                    codigo=200
                )
            else:
                return RespuestaOperacion(
                    exito='false',
                    mensaje=f'Estudiante {matricula} no encontrado',
                    codigo=404
                )

        except Error as e:
            logger.error(f"Error actualizando estudiante: {e}")
            return RespuestaOperacion(
                exito='false',
                mensaje=f'Error al actualizar estudiante: {str(e)}',
                codigo=400
            )
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @rpc(Unicode, _returns=RespuestaOperacion)
    def eliminar_estudiante(ctx, matricula):
        """
        Elimina un estudiante del sistema

        Args:
            matricula: Matricula del estudiante a eliminar

        Returns:
            RespuestaOperacion: Resultado de la operacion
        """
        logger.info(f"Eliminando estudiante: {matricula}")

        connection = get_db_connection()
        if not connection:
            return RespuestaOperacion(
                exito='false',
                mensaje='Error de conexion a la base de datos',
                codigo=500
            )

        try:
            cursor = connection.cursor()
            query = "DELETE FROM estudiantes WHERE matricula = %s"
            cursor.execute(query, (matricula,))
            connection.commit()

            if cursor.rowcount > 0:
                logger.info(f"Estudiante eliminado: {matricula}")
                return RespuestaOperacion(
                    exito='true',
                    mensaje=f'Estudiante {matricula} eliminado exitosamente',
                    codigo=200
                )
            else:
                return RespuestaOperacion(
                    exito='false',
                    mensaje=f'Estudiante {matricula} no encontrado',
                    codigo=404
                )

        except Error as e:
            logger.error(f"Error eliminando estudiante: {e}")
            return RespuestaOperacion(
                exito='false',
                mensaje=f'Error al eliminar estudiante: {str(e)}',
                codigo=400
            )
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @rpc(Unicode, _returns=Iterable(Estudiante))
    def buscar_estudiantes_por_estatus(ctx, estatus):
        """
        Busca estudiantes por su estatus

        Args:
            estatus: Estatus a buscar (activo, inactivo, egresado, baja)

        Returns:
            Iterable[Estudiante]: Lista de estudiantes con ese estatus
        """
        logger.info(f"Buscando estudiantes con estatus: {estatus}")

        connection = get_db_connection()
        if not connection:
            return []

        try:
            cursor = connection.cursor(dictionary=True)
            query = """
                SELECT id_estudiante, matricula, nombre, apellido_paterno,
                       apellido_materno, email, telefono,
                       DATE_FORMAT(fecha_nacimiento, '%Y-%m-%d') as fecha_nacimiento,
                       direccion,
                       DATE_FORMAT(fecha_ingreso, '%Y-%m-%d') as fecha_ingreso,
                       estatus
                FROM estudiantes
                WHERE estatus = %s
                ORDER BY apellido_paterno, apellido_materno, nombre
            """
            cursor.execute(query, (estatus,))
            results = cursor.fetchall()

            estudiantes = []
            for result in results:
                estudiante = Estudiante(
                    id_estudiante=result['id_estudiante'],
                    matricula=result['matricula'],
                    nombre=result['nombre'],
                    apellido_paterno=result['apellido_paterno'],
                    apellido_materno=result['apellido_materno'] or '',
                    email=result['email'],
                    telefono=result['telefono'] or '',
                    fecha_nacimiento=result['fecha_nacimiento'] or '',
                    direccion=result['direccion'] or '',
                    fecha_ingreso=result['fecha_ingreso'],
                    estatus=result['estatus']
                )
                estudiantes.append(estudiante)

            logger.info(f"Estudiantes encontrados con estatus {estatus}: {len(estudiantes)}")
            return estudiantes

        except Error as e:
            logger.error(f"Error buscando estudiantes: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()


# Configuracion de la aplicacion SOAP
application = Application(
    [EstudianteService],
    tns='http://uav.mx/servicios/estudiantes',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

# Crear aplicacion WSGI
wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    print("=" * 60)
    print("SERVICIO SOAP - SISTEMA DE ESTUDIANTES")
    print("Universidad Autonoma Veracruzana")
    print("=" * 60)
    print("\nIniciando servidor SOAP en http://localhost:8000")
    print("WSDL disponible en: http://localhost:8000/?wsdl")
    print("\nOperaciones disponibles:")
    print("  - obtener_estudiante(matricula)")
    print("  - listar_estudiantes()")
    print("  - crear_estudiante(...)")
    print("  - actualizar_estudiante(...)")
    print("  - eliminar_estudiante(matricula)")
    print("  - buscar_estudiantes_por_estatus(estatus)")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("=" * 60)

    server = make_server('localhost', 8000, wsgi_application)
    server.serve_forever()
