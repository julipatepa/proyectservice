import logging
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión MySQL
app.config['MYSQL_HOST'] = 'julipatepa.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'julipatepa'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'julipatepa$julipatepa'

# Inicializar MySQL
mysql = MySQL(app)

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar el formulario
@app.route('/log_user')
def log_user():
    return render_template('log_user.html')

# Ruta para procesar el formulario
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        nombre_completo = request.form['nombre_completo']
        telefono = request.form['telefono']
        detalle_problema = request.form['detalle_problema']

        try:
            # Crear cursor
            cur = mysql.connection.cursor()

            # Ejecutar consulta SQL para insertar datos
            cur.execute("INSERT INTO formulario (email, nombre_completo, telefono, detalle_problema) VALUES (%s, %s, %s, %s)",
                        (email, nombre_completo, telefono, detalle_problema))

            # Commit para guardar cambios en la base de datos
            mysql.connection.commit()

            # Cerrar cursor
            cur.close()

            app.logger.info(f"Datos insertados: {email}, {nombre_completo}, {telefono}, {detalle_problema}")

            # Redirigir a la página principal
            return redirect(url_for('ver_datos'))

        except Exception as e:
            app.logger.error(f"Error al insertar datos: {e}")
            return "Error al insertar datos en la base de datos."

# Ruta para la segunda página
@app.route('/pag_dos')
def pag_dos():
    return render_template('pag_dos.html')

# Ruta para ver los datos insertados
@app.route('/ver_datos', methods=['GET'])
def ver_datos():
    try:
        # Crear cursor
        cur = mysql.connection.cursor()

        # Ejecutar consulta SQL para seleccionar datos
        cur.execute("SELECT * FROM formulario")

        # Obtener todos los registros
        data = cur.fetchall()

        # Cerrar cursor
        cur.close()

        # Renderizar template con los datos
        return render_template('ver_datos.html', data=data)

    except Exception as e:
        app.logger.error(f"Error al obtener datos: {e}")
        return f"Error al obtener datos de la base de datos: {e}"

# Ruta para editar datos
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'POST':
        email = request.form['email']
        nombre_completo = request.form['nombre_completo']
        telefono = request.form['telefono']
        detalle_problema = request.form['detalle_problema']

        try:
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE formulario
                SET email = %s,
                    nombre_completo = %s,
                    telefono = %s,
                    detalle_problema = %s
                WHERE id = %s
            """, (email, nombre_completo, telefono, detalle_problema, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('ver_datos'))
        except Exception as e:
            app.logger.error(f"Error al actualizar datos: {e}")
            return f"Error al actualizar datos en la base de datos: {e}"
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM formulario WHERE id = %s", [id])
        data = cur.fetchone()
        cur.close()
        return render_template('editar.html', data=data)
    except Exception as e:
        app.logger.error(f"Error al obtener datos para editar: {e}")
        return f"Error al obtener datos para editar de la base de datos: {e}"

# Ruta para eliminar datos
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM formulario WHERE id = %s", [id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('ver_datos'))
    except Exception as e:
        app.logger.error(f"Error al eliminar datos: {e}")
        return f"Error al eliminar datos de la base de datos: {e}"

if __name__ == '__main__':
    app.run(debug=True, port=5001)
