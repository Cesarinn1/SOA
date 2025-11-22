"""
API SOAP - Sistema de Estudiantes/Matriculas
Universidad Autonoma Veracruzana
Arquitectura Orientada a Servicios

Este servicio implementa operaciones CRUD para la entidad Estudiantes
utilizando el protocolo SOAP con Python y Flask.
"""

from flask import Flask, request, Response
import mysql.connector
from mysql.connector import Error
import logging

# Configuracion de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuracion de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'database': 'uav_sistema_academico',
    'user': 'root',
    'password': 'MySQL2024!'
}

# Namespace para SOAP
NAMESPACE = "http://uav.mx/servicios/estudiantes"


def get_db_connection():
    """Establece conexion con la base de datos MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        logger.error(f"Error conectando a MySQL: {e}")
        return None


def crear_respuesta_soap(body_content):
    """Crea un envelope SOAP con el contenido dado"""
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
               xmlns:tns="{NAMESPACE}">
    <soap:Body>
        {body_content}
    </soap:Body>
</soap:Envelope>'''


def estudiante_to_xml(est):
    """Convierte un diccionario de estudiante a XML"""
    return f'''<tns:Estudiante>
            <tns:id_estudiante>{est['id_estudiante']}</tns:id_estudiante>
            <tns:matricula>{est['matricula']}</tns:matricula>
            <tns:nombre>{est['nombre']}</tns:nombre>
            <tns:apellido_paterno>{est['apellido_paterno']}</tns:apellido_paterno>
            <tns:apellido_materno>{est['apellido_materno'] or ''}</tns:apellido_materno>
            <tns:email>{est['email']}</tns:email>
            <tns:telefono>{est['telefono'] or ''}</tns:telefono>
            <tns:fecha_nacimiento>{est['fecha_nacimiento'] or ''}</tns:fecha_nacimiento>
            <tns:direccion>{est['direccion'] or ''}</tns:direccion>
            <tns:fecha_ingreso>{est['fecha_ingreso']}</tns:fecha_ingreso>
            <tns:estatus>{est['estatus']}</tns:estatus>
        </tns:Estudiante>'''


def obtener_estudiante_db(matricula):
    """Obtiene un estudiante por matricula"""
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
        return cursor.fetchone()
    except Error as e:
        logger.error(f"Error en consulta: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def listar_estudiantes_db():
    """Lista todos los estudiantes"""
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
        return cursor.fetchall()
    except Error as e:
        logger.error(f"Error listando estudiantes: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def crear_estudiante_db(datos):
    """Crea un nuevo estudiante"""
    connection = get_db_connection()
    if not connection:
        return False, "Error de conexion"

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO estudiantes
            (matricula, nombre, apellido_paterno, apellido_materno,
             email, telefono, fecha_nacimiento, direccion, fecha_ingreso, estatus)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'activo')
        """
        cursor.execute(query, (
            datos.get('matricula'), datos.get('nombre'),
            datos.get('apellido_paterno'), datos.get('apellido_materno'),
            datos.get('email'), datos.get('telefono'),
            datos.get('fecha_nacimiento') or None, datos.get('direccion'),
            datos.get('fecha_ingreso')
        ))
        connection.commit()
        return True, f"Estudiante {datos.get('matricula')} creado exitosamente"
    except Error as e:
        return False, str(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def actualizar_estudiante_db(datos):
    """Actualiza un estudiante"""
    connection = get_db_connection()
    if not connection:
        return False, "Error de conexion"

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
            datos.get('nombre'), datos.get('apellido_paterno'),
            datos.get('apellido_materno'), datos.get('email'),
            datos.get('telefono'), datos.get('fecha_nacimiento') or None,
            datos.get('direccion'), datos.get('fecha_ingreso'),
            datos.get('estatus'), datos.get('matricula')
        ))
        connection.commit()
        if cursor.rowcount > 0:
            return True, f"Estudiante {datos.get('matricula')} actualizado"
        return False, "Estudiante no encontrado"
    except Error as e:
        return False, str(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def eliminar_estudiante_db(matricula):
    """Elimina un estudiante"""
    connection = get_db_connection()
    if not connection:
        return False, "Error de conexion"

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE matricula = %s", (matricula,))
        connection.commit()
        if cursor.rowcount > 0:
            return True, f"Estudiante {matricula} eliminado"
        return False, "Estudiante no encontrado"
    except Error as e:
        return False, str(e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def buscar_por_estatus_db(estatus):
    """Busca estudiantes por estatus"""
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
        return cursor.fetchall()
    except Error as e:
        logger.error(f"Error buscando estudiantes: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def extraer_valor_xml(xml_str, tag):
    """Extrae el valor de un tag XML"""
    import re
    pattern = f'<[^>]*{tag}[^>]*>([^<]*)</[^>]*{tag}>'
    match = re.search(pattern, xml_str)
    return match.group(1) if match else None


@app.route('/', methods=['GET', 'POST'])
def soap_endpoint():
    """Endpoint principal SOAP"""

    # Si es GET con ?wsdl, devolver WSDL
    if request.method == 'GET' and 'wsdl' in request.args:
        wsdl = f'''<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://schemas.xmlsoap.org/wsdl/"
             xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
             xmlns:tns="{NAMESPACE}"
             xmlns:xsd="http://www.w3.org/2001/XMLSchema"
             name="EstudianteService"
             targetNamespace="{NAMESPACE}">

    <types>
        <xsd:schema targetNamespace="{NAMESPACE}">
            <xsd:complexType name="Estudiante">
                <xsd:sequence>
                    <xsd:element name="id_estudiante" type="xsd:int"/>
                    <xsd:element name="matricula" type="xsd:string"/>
                    <xsd:element name="nombre" type="xsd:string"/>
                    <xsd:element name="apellido_paterno" type="xsd:string"/>
                    <xsd:element name="apellido_materno" type="xsd:string"/>
                    <xsd:element name="email" type="xsd:string"/>
                    <xsd:element name="telefono" type="xsd:string"/>
                    <xsd:element name="fecha_nacimiento" type="xsd:string"/>
                    <xsd:element name="direccion" type="xsd:string"/>
                    <xsd:element name="fecha_ingreso" type="xsd:string"/>
                    <xsd:element name="estatus" type="xsd:string"/>
                </xsd:sequence>
            </xsd:complexType>
        </xsd:schema>
    </types>

    <message name="obtener_estudiante_request">
        <part name="matricula" type="xsd:string"/>
    </message>
    <message name="obtener_estudiante_response">
        <part name="estudiante" type="tns:Estudiante"/>
    </message>

    <message name="listar_estudiantes_request"/>
    <message name="listar_estudiantes_response">
        <part name="estudiantes" type="tns:Estudiante"/>
    </message>

    <message name="crear_estudiante_request">
        <part name="estudiante" type="tns:Estudiante"/>
    </message>
    <message name="crear_estudiante_response">
        <part name="resultado" type="xsd:string"/>
    </message>

    <portType name="EstudiantePortType">
        <operation name="obtener_estudiante">
            <input message="tns:obtener_estudiante_request"/>
            <output message="tns:obtener_estudiante_response"/>
        </operation>
        <operation name="listar_estudiantes">
            <input message="tns:listar_estudiantes_request"/>
            <output message="tns:listar_estudiantes_response"/>
        </operation>
        <operation name="crear_estudiante">
            <input message="tns:crear_estudiante_request"/>
            <output message="tns:crear_estudiante_response"/>
        </operation>
    </portType>

    <binding name="EstudianteBinding" type="tns:EstudiantePortType">
        <soap:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
        <operation name="obtener_estudiante">
            <soap:operation soapAction="obtener_estudiante"/>
        </operation>
        <operation name="listar_estudiantes">
            <soap:operation soapAction="listar_estudiantes"/>
        </operation>
        <operation name="crear_estudiante">
            <soap:operation soapAction="crear_estudiante"/>
        </operation>
    </binding>

    <service name="EstudianteService">
        <port name="EstudiantePort" binding="tns:EstudianteBinding">
            <soap:address location="http://localhost:8000/"/>
        </port>
    </service>
</definitions>'''
        return Response(wsdl, mimetype='text/xml')

    # Procesar peticion SOAP POST
    if request.method == 'POST':
        xml_data = request.data.decode('utf-8')
        logger.info(f"Request recibido: {xml_data[:200]}...")

        # Detectar operacion
        if 'listar_estudiantes' in xml_data:
            estudiantes = listar_estudiantes_db()
            estudiantes_xml = '\n'.join([estudiante_to_xml(e) for e in estudiantes])
            body = f'''<tns:listar_estudiantes_response>
            {estudiantes_xml}
        </tns:listar_estudiantes_response>'''
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        elif 'obtener_estudiante' in xml_data:
            matricula = extraer_valor_xml(xml_data, 'matricula')
            if matricula:
                estudiante = obtener_estudiante_db(matricula)
                if estudiante:
                    body = f'''<tns:obtener_estudiante_response>
                    {estudiante_to_xml(estudiante)}
                </tns:obtener_estudiante_response>'''
                else:
                    body = f'''<tns:obtener_estudiante_response>
                    <tns:error>Estudiante no encontrado</tns:error>
                </tns:obtener_estudiante_response>'''
            else:
                body = '<tns:error>Matricula no proporcionada</tns:error>'
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        elif 'crear_estudiante' in xml_data:
            datos = {
                'matricula': extraer_valor_xml(xml_data, 'matricula'),
                'nombre': extraer_valor_xml(xml_data, 'nombre'),
                'apellido_paterno': extraer_valor_xml(xml_data, 'apellido_paterno'),
                'apellido_materno': extraer_valor_xml(xml_data, 'apellido_materno'),
                'email': extraer_valor_xml(xml_data, 'email'),
                'telefono': extraer_valor_xml(xml_data, 'telefono'),
                'fecha_nacimiento': extraer_valor_xml(xml_data, 'fecha_nacimiento'),
                'direccion': extraer_valor_xml(xml_data, 'direccion'),
                'fecha_ingreso': extraer_valor_xml(xml_data, 'fecha_ingreso')
            }
            exito, mensaje = crear_estudiante_db(datos)
            body = f'''<tns:crear_estudiante_response>
                <tns:exito>{'true' if exito else 'false'}</tns:exito>
                <tns:mensaje>{mensaje}</tns:mensaje>
            </tns:crear_estudiante_response>'''
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        elif 'actualizar_estudiante' in xml_data:
            datos = {
                'matricula': extraer_valor_xml(xml_data, 'matricula'),
                'nombre': extraer_valor_xml(xml_data, 'nombre'),
                'apellido_paterno': extraer_valor_xml(xml_data, 'apellido_paterno'),
                'apellido_materno': extraer_valor_xml(xml_data, 'apellido_materno'),
                'email': extraer_valor_xml(xml_data, 'email'),
                'telefono': extraer_valor_xml(xml_data, 'telefono'),
                'fecha_nacimiento': extraer_valor_xml(xml_data, 'fecha_nacimiento'),
                'direccion': extraer_valor_xml(xml_data, 'direccion'),
                'fecha_ingreso': extraer_valor_xml(xml_data, 'fecha_ingreso'),
                'estatus': extraer_valor_xml(xml_data, 'estatus')
            }
            exito, mensaje = actualizar_estudiante_db(datos)
            body = f'''<tns:actualizar_estudiante_response>
                <tns:exito>{'true' if exito else 'false'}</tns:exito>
                <tns:mensaje>{mensaje}</tns:mensaje>
            </tns:actualizar_estudiante_response>'''
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        elif 'eliminar_estudiante' in xml_data:
            matricula = extraer_valor_xml(xml_data, 'matricula')
            exito, mensaje = eliminar_estudiante_db(matricula)
            body = f'''<tns:eliminar_estudiante_response>
                <tns:exito>{'true' if exito else 'false'}</tns:exito>
                <tns:mensaje>{mensaje}</tns:mensaje>
            </tns:eliminar_estudiante_response>'''
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        elif 'buscar_estudiantes_por_estatus' in xml_data:
            estatus = extraer_valor_xml(xml_data, 'estatus')
            estudiantes = buscar_por_estatus_db(estatus)
            estudiantes_xml = '\n'.join([estudiante_to_xml(e) for e in estudiantes])
            body = f'''<tns:buscar_estudiantes_por_estatus_response>
                {estudiantes_xml}
            </tns:buscar_estudiantes_por_estatus_response>'''
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

        else:
            body = '<tns:error>Operacion no reconocida</tns:error>'
            return Response(crear_respuesta_soap(body), mimetype='text/xml')

    # GET sin WSDL - mostrar info
    return '''
    <h1>API SOAP - Sistema de Estudiantes</h1>
    <h2>Universidad Autonoma Veracruzana</h2>
    <p>WSDL: <a href="/?wsdl">/?wsdl</a></p>
    <h3>Operaciones disponibles:</h3>
    <ul>
        <li>obtener_estudiante(matricula)</li>
        <li>listar_estudiantes()</li>
        <li>crear_estudiante(...)</li>
        <li>actualizar_estudiante(...)</li>
        <li>eliminar_estudiante(matricula)</li>
        <li>buscar_estudiantes_por_estatus(estatus)</li>
    </ul>
    '''


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

    app.run(host='0.0.0.0', port=8000, debug=False)
