from flask import Flask, render_template, url_for, request, redirect, session
app = Flask(__name__)

usuarios = [
    {'id':1, 'nombre':'Misael', 'apellido':'Barajas', 'usuario':'MisaelB', 'telefono':'3511563006', 'correo':'misael@gmail.com', 'password':'misael05b'},
    {'id':2, 'nombre':'Alberto', 'apellido':'Molina', 'usuario':'AlbertoM', 'telefono':'3513093789', 'correo':'alberto@gmail.com', 'password':'alberto05m', 'rol':'admin'},
]

app.secret_key = 'mi_clave_secreta'

@app.route('/')
def raiz():
    return render_template('index.html', usuario=session.get('usuario'))

@app.route('/inicio')
def inicio():
    return render_template('index.html', usuario=session.get('usuario'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        password = request.form['password']
        for usuario in usuarios:
            if usuario['correo'] == correo and usuario['password'] == password:
                session['usuario'] = {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'apellido': usuario['apellido'],
                    'usuario': usuario['usuario'],
                    'telefono': usuario['telefono'],
                    'correo': usuario['correo']
                }
                return redirect(url_for('inicio'))
        return render_template('login.html', error='Correo o contraseña incorrectos')
    temp = session.pop('registro_temp', {})
    correo = temp.get('correo', '')
    password = temp.get('password', '')
    return render_template('login.html', error=None, correo=correo, password=password)


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        usuario = request.form['usuario']
        telefono = request.form['telefono']
        correo = request.form['correo']
        password = request.form['password']
        id = len(usuarios)
        nuevoUsuario = {'id':id, 'nombre':nombre, 'usuario':usuario , 'apellido':apellido, 'telefono':telefono, 'correo':correo, 'password':password}
        usuarios.append(nuevoUsuario)
        session['registro_temp'] = {'correo': correo, 'password': password}
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('usuario', None)
    return redirect(url_for('inicio'))

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/info/politicas-de-uso')
def politicas_uso():
    return render_template('politicas-de-uso.html')

@app.route('/info/aviso-de-privacidad')
def aviso_privacidad():
    return render_template('aviso-de-privacidad.html')

@app.route('/info/contactar')
def contactar():
    return render_template('contactar.html')

@app.route('/cuenta/perfil')
def perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('perfil.html', usuario=session['usuario'])

@app.route('/sugerencias')
def sugerencias():
    return render_template('sugerencias.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

'''
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
'''

if __name__ == '__main__':
    app.run(debug=True)