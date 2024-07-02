from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Host de MySQL
app.config['MYSQL_USER'] = 'root'       # Usuario de MySQL
app.config['MYSQL_PASSWORD'] = '446303699799'  # Contraseña de MySQL
app.config['MYSQL_DB'] = 'formulario_db'  # Nombre de la base de datos
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar MySQL
mysql = MySQL(app)

# Ruta para el formulario y procesamiento de datos
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para procesar el formulario
@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        nombre_completo = request.form['nombre_completo']
        telefono = request.form['telefono']
        detalle_problema = request.form['detalle_problema']

        # Crear cursor
        cur = mysql.connection.cursor()

        # Ejecutar consulta SQL para insertar datos
        cur.execute("INSERT INTO formulario (email, nombre_completo, telefono, detalle_problema) VALUES (%s, %s, %s, %s)",
                    (email, nombre_completo, telefono, detalle_problema))

        # Commit para guardar cambios en la base de datos
        mysql.connection.commit()

        # Cerrar cursor
        cur.close()

        # Redirigir a una página de éxito o a donde desees
        return redirect(url_for('success'))

# Ruta para la página de éxito
@app.route('/success')
def success():
    return 'Formulario enviado con éxito'

@app.route('/pag_dos')
def pag_dos():
    return render_template('pag_dos.html')

@app.route('/log_user')
def log_user():
    return render_template('log_user.html')

if __name__ == '__main__':
    app.run(debug=True)
