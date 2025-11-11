from flask import Flask, render_template, url_for, request, redirect, session, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash
from modelo.Dao import db, Usuario, Categoria, Receta, calificacion


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:Misa19a13@localhost/WikiRecetas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

app.secret_key = 'MiClaveSecretaWikiRecetas'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '¡ Debes iniciar sesión para acceder a esta página !'
login_manager.login_message_category = "info"

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario().consultaIndividual(id)

@app.before_request
def before_request():
    session.permanent=True
    app.permanent_session_lifetime=timedelta(minutes=10)

@app.context_processor
def inject_user():
    return dict(user=current_user)

@app.route('/')
def index():
    recetas = Receta().consultaGeneral()
    categorias = Categoria().consultaGeneral()
    return render_template('index.html', recetas=recetas, categorias=categorias)

@app.route('/inicio')
def inicio():
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))
        
    if request.method == 'POST':
        email_form = request.form['correo']
        password_form = request.form['password']
        
        u = Usuario().validar(email_form, password_form)
        if u is not None:
            login_user(u)
            return redirect(url_for('inicio'))
        return render_template('login.html', userError='Usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        nombreUsuario = request.form['usuario']
        email = request.form['correo']
        telefono = request.form['telefono']
        password = request.form['password']
        nuevo_usuario = Usuario()
        nuevo_usuario.nombre = nombre
        nuevo_usuario.apellido = apellido
        nuevo_usuario.nombreUsuario = nombreUsuario
        nuevo_usuario.email = email
        nuevo_usuario.telefono = telefono
        nuevo_usuario.password = generate_password_hash(password)
        nuevo_usuario.nombre_apellido = f"{nombre} {apellido}"
        
        foto_file = request.files.get('fotoUsuario')
        if foto_file and foto_file.filename != '':
            nuevo_usuario.fotoUsuario = foto_file.stream.read()
        else:
            nuevo_usuario.fotoUsuario = None 
        
        nuevo_usuario.agregar()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/cuenta/perfil')
@login_required
def perfil():
    if current_user.is_authenticated:
        return render_template('perfil.html', u = current_user)
    return redirect(url_for('login'))

@app.route('/cuenta/perfil/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(id):
    u = Usuario().consultaIndividual(id)
    if request.method == 'POST':
        u.nombre = request.form['nombre']
        u.apellido = request.form['apellido']
        u.nombreUsuario = request.form['usuario']
        u.email = request.form['correo']
        u.telefono = request.form['telefono']

        if 'fotoUsuario' in request.files:
             file = request.files['fotoUsuario']
             if file.filename != '':
                u.fotoUsuario=request.files['fotoUsuario'].stream.read()
        
        u.editar()
        return redirect(url_for('perfil'))
    return render_template('editar-perfil.html', u = current_user)

@app.route('/usuarios/obtenerImagen/<int:idUsuario>')
def obtenerImagenUsuario(idUsuario):
    u = Usuario()
    if u:
        return u.consultarImagen(idUsuario)
    else:
        return redirect(url_for('static', filename='uploads/foto_perfil_default.jpg'))

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/nueva_receta', methods=['GET', 'POST'])
@login_required 
def nueva_receta():    
    if request.method == 'POST':
        r = Receta()
        r.nombre = request.form['nombreReceta']
        r.descripcion = request.form['descripcion']
        r.dificultad = request.form['dificultad']
        r.ingredientes = request.form['ingredientes']
        r.preparacion = request.form['preparacion']
        r.idCategoria = request.form['categoria']
        r.idUsuario = current_user.idUsuario 
        
        r.agregar()

        imagen_file = request.files.get('imagen')

        if imagen_file:
            r.imagen = imagen_file.stream.read()
            r.agregar()
        
        return redirect(url_for('mis_recetas'))
    
    categorias = Categoria().consultaGeneral()
    return render_template('nueva-receta.html', categorias=categorias)

@app.route('/receta/obtenerImagen/<int:idReceta>')
def obtenerImagenReceta(idReceta):
    r = Receta()
    return r.consultarImagen(idReceta)

@app.route("/mis-recetas")
@login_required
def mis_recetas():
    misrecetas = Receta.query.filter_by(idUsuario=current_user.idUsuario).all()
    return render_template('mis-recetas.html', misrecetas=misrecetas)

@app.route('/editar_receta/<int:idReceta>', methods=['POST', 'GET'])
@login_required
def editar_receta(idReceta):
    rec_dao = Receta()
    r = rec_dao.consultaIndividual(idReceta)

    if r is None: abort(404) 
    if r.idUsuario != current_user.idUsuario:
        flash('No tienes permiso para editar esta receta.', 'danger')
        return redirect(url_for('mis_recetas'))

    if request.method == 'GET':
        categorias = Categoria().consultaGeneral()
        return render_template('editar-receta.html', receta=r, categorias=categorias)      
    if request.method == 'POST':
        r.nombre = request.form['nombreReceta']
        r.descripcion = request.form['descripcion']
        r.dificultad = request.form['dificultad']
        r.ingredientes = request.form['ingredientes']
        r.preparacion = request.form['preparacion']
        r.idCategoria = request.form['categoria']
        
        r.editar() 
        return redirect(url_for('mis_recetas'))

@app.route('/eliminar_receta/<int:idReceta>', methods=['POST', 'GET'])
@login_required
def eliminar_receta(idReceta):
    rec_dao = Receta()
    r = rec_dao.consultaIndividual(idReceta)

    if r is None: abort(404)
    if r.idUsuario != current_user.idUsuario:
        return redirect(url_for('mis_recetas'))

    if request.method == 'POST':
        rec_dao.eliminar(idReceta)
        return redirect(url_for('mis_recetas'))
    
    return render_template('eliminar-receta.html', receta=r)

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/sugerencias')
def sugerencias():
    return render_template('sugerencias.html')

@app.route('/categorias')
def ver_categorias():
    return render_template('categorias.html')

@app.route('/info/politicas-de-uso')
def politicas_uso():
    return render_template('politicas-de-uso.html')

@app.route('/info/aviso-de-privacidad')
def aviso_privacidad():
    return render_template('aviso-de-privacidad.html')

@app.route('/info/contactar')
def contactar():
    return render_template('contactar.html')

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True)