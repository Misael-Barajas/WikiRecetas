from flask import Flask, render_template, url_for, request, redirect, session, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash
from modelo.Dao import db, Usuario, Categoria, Receta, imagenVideo, calificacion


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
        u = Usuario()
        u.fotoUsuario=request.files['fotoUsuario'].stream.read()
        u.nombre = request.form['nombre']
        u.apellido = request.form['apellido']
        u.nombreUsuario = request.form['usuario']
        u.email = request.form['correo']
        u.telefono = request.form['telefono']
        u.password = generate_password_hash(request.form['password'])
        u.nombre_apellido = f"{u.nombre} {u.apellido}"
        
        if 'fotoUsuario' in request.files:
             foto = request.files['fotoUsuario']
             if foto.filename != '':
                 u.fotoUsuario = foto.stream.read()
        
        u.agregar()
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/cuenta/perfil')
@login_required
def perfil():
    if current_user.is_authenticated:
        return render_template('perfil.html', u = current_user)
    return redirect(url_for('login'))

@app.route('/cuenta/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        u = current_user
        u.fotoUsuario=request.files['fotoUsuario'].stream.read()
        u.nombre = request.form['nombre']
        u.apellido = request.form['apellido']
        u.nombreUsuario = request.form['usuario']
        u.email = request.form['correo']
        u.telefono = request.form['telefono']
        u.nombre_apellido = f"{u.nombre} {u.apellido}"
        
        if 'fotoUsuario' in request.files:
             foto = request.files['fotoUsuario']
             if foto.filename != '':
                 u.fotoUsuario = foto.stream.read()
        u.editar()
        return redirect(url_for('perfil'))
    return render_template('editar-perfil.html', u = current_user)


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
        video_file = request.files.get('videos')

        if imagen_file:
            iv = imagenVideo()
            iv.imagen = imagen_file.stream.read()
            if video_file:
                iv.video = video_file.stream.read()
            
            iv.idReceta = r.idReceta 
            iv.agregar()
        
        return redirect(url_for('mis_recetas'))
    
    categorias = Categoria().consultaGeneral()
    return render_template('nueva-receta.html', categorias=categorias)

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

@app.route('/usuarios/obtenerImagen/<int:idUsuario>')
def obtenerImagenUsuario(idUsuario):
    u = Usuario()
    return u.consultarImagen(idUsuario)

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