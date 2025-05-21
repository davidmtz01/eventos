from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='bfaxn3guvrgq9avkkrkk-mysql.services.clever-cloud.com',
        user='uqstbj5ei42rgiio',
        password='Uptx37HGb0mueF2kqwKF',
        database='bfaxn3guvrgq9avkkrkk'
    )

@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Usuario (nombre, email, password)
        VALUES (%s, %s, %s)
    """, (data['nombre'], data['email'], data['password']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario creado', 'usuario_id': nuevo_id}), 201

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def editar_usuario(usuario_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE Usuario
        SET nombre = %s, email = %s, password = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data['nombre'],
        data['email'],
        data['password'],
        usuario_id
    ))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas:
        return jsonify({'mensaje': 'Usuario actualizado'}), 200
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuario WHERE id = %s", (usuario_id,))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()
    if filas:
        return jsonify({'mensaje': 'Usuario eliminado'}), 200
    return jsonify({'mensaje': 'Usuario no encontrado'}), 404

@app.route('/eventos', methods=['POST'])
def crear_evento():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Evento (titulo, descripcion, fecha, hora, ubicacion, tipo, organizador_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (data['titulo'], data.get('descripcion'), data['fecha'], data['hora'],
          data.get('ubicacion'), data['tipo'], data['organizador_id']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Evento creado', 'evento_id': nuevo_id}), 201

@app.route('/eventos', methods=['GET'])
def obtener_eventos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Evento")
    eventos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(eventos)

@app.route('/eventos/<int:evento_id>', methods=['PUT'])
def editar_evento(evento_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE Evento
        SET titulo = %s, descripcion = %s, fecha = %s, hora = %s,
            ubicacion = %s, tipo = %s, organizador_id = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data['titulo'],
        data.get('descripcion'),
        data['fecha'],
        data['hora'],
        data.get('ubicacion'),
        data['tipo'],
        data['organizador_id'],
        evento_id
    ))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas:
        return jsonify({'mensaje': 'Evento actualizado'}), 200
    return jsonify({'mensaje': 'Evento no encontrado'}), 404

@app.route('/eventos/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(evento_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Evento WHERE id = %s", (evento_id,))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()
    if filas:
        return jsonify({'mensaje': 'Evento eliminado'}), 200
    return jsonify({'mensaje': 'Evento no encontrado'}), 404

@app.route('/asistentes', methods=['POST'])
def crear_asistente():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Asistente (evento_id, usuario_id)
        VALUES (%s, %s)
    """, (data['evento_id'], data['usuario_id']))
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return jsonify({'mensaje': 'Asistente creado', 'asistente_id': nuevo_id}), 201

@app.route('/asistentes', methods=['GET'])
def obtener_asistentes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Asistente")
    asistentes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(asistentes)

@app.route('/asistentes/<int:asistente_id>', methods=['PUT'])
def editar_asistente(asistente_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE Asistente
        SET evento_id = %s, usuario_id = %s
        WHERE id = %s
    """
    cursor.execute(sql, (
        data['evento_id'],
        data['usuario_id'],
        asistente_id
    ))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()

    if filas:
        return jsonify({'mensaje': 'Asistente actualizado'}), 200
    return jsonify({'mensaje': 'Asistente no encontrado'}), 404

@app.route('/asistentes/<int:asistente_id>', methods=['DELETE'])
def eliminar_asistente(asistente_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Asistente WHERE id = %s", (asistente_id,))
    conn.commit()
    filas = cursor.rowcount
    cursor.close()
    conn.close()
    if filas:
        return jsonify({'mensaje': 'Asistente eliminado'}), 200
    return jsonify({'mensaje': 'Asistente no encontrado'}), 404

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
