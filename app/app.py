from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pag_dos')
def pag_dos():
    return render_template('pag_dos.html')

@app.route('/log_user')
def log_user():
    return render_template('log_user.html')

if __name__ == '__main__':
    app.run(debug=True)
