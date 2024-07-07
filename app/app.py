from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la conexión MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Host de MySQL
app.config['MYSQL_USER'] = 'root'       # Usuario de MySQL
app.config['MYSQL_PASSWORD'] = ''  # Contraseña de MySQL
app.config['MYSQL_DB'] = 'formulario_db'  # Nombre de la base de datos
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Inicializar MySQL
mysql = MySQL(app)

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
        numero_telefono = request.form['numero_telefono']
        problema = request.form['problema']

        # Crear cursor
        cur = mysql.connection.cursor()

        # Ejecutar consulta SQL para insertar datos
        cur.execute("INSERT INTO formulario (email, nombre_completo, numero_telefono, problema) VALUES (%s, %s, %s, %s)",
                    (email, nombre_completo, numero_telefono, problema))

        # Commit para guardar cambios en la base de datos
        mysql.connection.commit()

        # Cerrar cursor
        cur.close()

        # Redirigir a la página principal
        return redirect(url_for('index'))

# Ruta para la segunda página
@app.route('/pag_dos')
def pag_dos():
    return render_template('pag_dos.html')

if __name__ == '__main__':
    app.run(debug=True)
