from flask import Flask, render_template, url_for, request, redirect, session
app = Flask(__name__)

usuarios = [
    {'id':1, 'nombre':'Misael', 'apellido':'Barajas', 'usuario':'MisaelB', 'telefono':'3511563006', 'correo':'misael@gmail.com', 'password':'misael05b', 'rol':'admin'},
    {'id':2, 'nombre':'Alberto', 'apellido':'Molina', 'usuario':'AlbertoM', 'telefono':'3513093789', 'correo':'alberto@gmail.com', 'password':'alberto05m', 'rol':'admin'},
]

recetas = [
    {'id':1, 'nombre':'Nombre receta', 'descripcion':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Vero ducimus fuga officiis provident veritatis quae nisi perferendis fugiat?', 'dificultad':'facil', 'ingredientes':['Ingrediente1', 'Ingrediente2', 'Ingrediente3', 'Ingrediente4', 'Ingrediente5'], 'preparacion':'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Dolorum itaque magni voluptate obcaecati architecto commodi quo eius temporibus earum quidem.', 'categoria':'Categoría', 'imagen':'img1.jpg', 'calificacion':'5'},
    {'id':2, 'nombre':'Nombre receta', 'descripcion':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Aspernatur rem expedita dolorem modi magni saepe!', 'dificultad':'facil', 'ingredientes':['Ingrediente1', 'Ingrediente2', 'Ingrediente3', 'Ingrediente4', 'Ingrediente5'], 'preparacion':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Corporis eaque amet fugiat dolores recusandae reprehenderit possimus eum vel temporibus voluptatem!', 'categoria':'Categoría', 'imagen':'img2.jpg', 'calificacion':'4.7'},
    {'id':3, 'nombre':'Nombre receta', 'descripcion':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Possimus accusamus nemo ut in quo? Similique!', 'dificultad':'facil', 'ingredientes':['Ingrediente1', 'Ingrediente2', 'Ingrediente3', 'Ingrediente4', 'Ingrediente5'], 'preparacion':'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maxime soluta accusamus ratione, illum molestiae velit labore atque ipsa itaque consectetur.', 'categoria':'Categoría', 'imagen':'img3.jpg', 'calificacion':'4.9'},
    {'id':4, 'nombre':'Nombre receta', 'descripcion':'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Laudantium nostrum libero reiciendis vitae, deserunt tempora reprehenderit aliquam atque eligendi! Voluptatem!', 'dificultad':'facil', 'ingredientes':['Ingrediente1', 'Ingrediente2', 'Ingrediente3', 'Ingrediente4', 'Ingrediente5'], 'preparacion':'Lorem ipsum dolor sit amet consectetur adipisicing elit. Nihil minus numquam explicabo ducimus reiciendis nemo quia cumque ipsa ex animi?', 'categoria':'Categoría', 'imagen':'img4.jpg', 'calificacion':'4.5'},
]

misrecetas = []



app.secret_key = 'mi_clave_secreta'

@app.route('/')
def raiz():
    return render_template('index.html', usuario=session.get('usuario'), recetas=recetas)

@app.route('/inicio')
def inicio():
    return render_template('index.html', usuario=session.get('usuario'), recetas=recetas)

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
                    'correo': usuario['correo'],
                    'password': usuario['password'],
                    'nombre_apellido': f"{usuario['nombre']} {usuario['apellido']}"
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
        id = usuarios[-1]['id'] + 1 if usuarios else 1
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

@app.route('/cuenta/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    user_id = session['usuario']['id']
    usuario_a_editar = next((u for u in usuarios if u['id'] == user_id), None)

    if usuario_a_editar is None:
        session.pop('usuario', None)
        return redirect(url_for('login'))

    if request.method == 'POST':
        usuario_a_editar['usuario'] = request.form.get('usuario')
        usuario_a_editar['nombre'] = request.form.get('nombre')
        usuario_a_editar['apellido'] = request.form.get('apellido')
        usuario_a_editar['correo'] = request.form.get('correo')
        usuario_a_editar['telefono'] = request.form.get('telefono')
        
        nueva_password = request.form.get('password')
        if nueva_password:
            usuario_a_editar['password'] = nueva_password

        session['usuario'] = {
            'id': usuario_a_editar['id'],
            'nombre': usuario_a_editar['nombre'],
            'apellido': usuario_a_editar['apellido'],
            'usuario': usuario_a_editar['usuario'],
            'telefono': usuario_a_editar['telefono'],
            'correo': usuario_a_editar['correo'],
            'password': usuario_a_editar['password'],
            'nombre_apellido': f"{usuario_a_editar['nombre']} {usuario_a_editar['apellido']}"
        }
        session.modified = True
        return redirect(url_for('perfil'))
    return render_template('editar-perfil.html', usuario=usuario_a_editar)


@app.route('/sugerencias')
def sugerencias():
    return render_template('sugerencias.html')

@app.route('/categorias')
def categorias():
    return render_template('categorias.html')

@app.route('/nueva_receta', methods=['GET', 'POST'])
def nueva_receta():    
    if 'usuario' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        dificultad = request.form['dificultad']
        ingredientes = request.form.getlist('ingredientes[]')
        preparacion = request.form['preparacion']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        videos = request.form.getlist('videos[]')
        id = misrecetas[-1]['id'] + 1 if misrecetas else 1
        nuevaReceta = {'id':id, 'nombre':nombre, 'descripcion':descripcion, 'dificultad':dificultad, 'ingredientes':ingredientes,'preparacion':preparacion, 'categoria':categoria, 'imagen':imagen, 'videos':videos}
        misrecetas.append(nuevaReceta)
        return redirect(url_for('mis_recetas'))
    return render_template('nueva-receta.html', usuario=session['usuario'])

@app.route("/mis-recetas")
def mis_recetas():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('mis-recetas.html', usuario=session['usuario'], misrecetas=misrecetas)
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