from flask import Flask, render_template, url_for, request, redirect, session, flash, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from werkzeug.security import generate_password_hash
from modelo.Dao import db, Usuario, Categoria, Receta, Calificacion, Sugerencia
from sqlalchemy import or_


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
    return render_template('index.html', recetas=recetas, categorias=categorias, calif=Calificacion)

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
    u = Usuario().consultaIndividual(idUsuario)
    if u and u.fotoUsuario:
        return u.fotoUsuario
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

        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename != '':
            r.imagen = imagen_file.stream.read()
        
        r.agregar()
        
        return redirect(url_for('mis_recetas'))
    
    categorias = Categoria().consultaGeneral()
    return render_template('nueva-receta.html', categorias=categorias)

@app.route("/mis-recetas")
@login_required
def mis_recetas():
    misrecetas = Receta.query.filter_by(idUsuario=current_user.idUsuario).all()
    return render_template('mis-recetas.html', misrecetas=misrecetas, calif = Calificacion)

@app.route('/editar-receta/<int:idReceta>', methods=['POST', 'GET'])
@login_required
def editar_receta(idReceta):
    r = Receta().consultaIndividual(idReceta)

    if r is None: abort(404) 
    
    if r.idUsuario != current_user.idUsuario and not current_user.is_admin():
        return redirect(url_for('mis_recetas'))
   
    if request.method == 'POST':
        r.nombre = request.form['nombreReceta']
        r.descripcion = request.form['descripcion']
        r.dificultad = request.form['dificultad']
        r.ingredientes = request.form['ingredientes']
        r.preparacion = request.form['preparacion']
        r.idCategoria = request.form['categoria']
        
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename != '':
            r.imagen = imagen_file.stream.read()
        
        r.editar(r.idReceta) 
        
        if current_user.is_admin() and r.idUsuario != current_user.idUsuario:
            return redirect(url_for('admin_recetas'))
            
        return redirect(url_for('mis_recetas'))
        
    categorias = Categoria().consultaGeneral()
    return render_template('editar-receta.html', receta=r, categorias=categorias)
    
@app.route('/receta/obtenerImagen/<int:idReceta>')
def obtenerImagenReceta(idReceta):
    r = Receta()
    return r.consultarImagen(idReceta)


@app.route('/eliminar_receta/<int:idReceta>', methods=['POST', 'GET'])
@login_required
def eliminar_receta(idReceta):
    rec_dao = Receta()
    r = rec_dao.consultaIndividual(idReceta)

    if r is None: abort(404)
    
    if r.idUsuario != current_user.idUsuario and not current_user.is_admin():
        return redirect(url_for('mis_recetas'))

    if request.method == 'POST':
        rec_dao.eliminar(idReceta)
        return redirect(url_for('mis_recetas'))
    
    return render_template('eliminar-receta.html', receta=r)

@app.route('/receta/<int:idReceta>', methods=['GET', 'POST'])
def ver_receta(idReceta):
    r = Receta().consultaIndividual(idReceta)
    if r is None:
        abort(404)
    
    promedio = Calificacion.obtener_promedio(idReceta)
    
    calificacion_usuario = None
    if current_user.is_authenticated:
        calificacion_usuario = Calificacion.query.filter_by(
            idUsuario=current_user.idUsuario, 
            idReceta=idReceta
        ).first()

    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        
        # Obtenemos los datos del form
        calif_value = request.form.get('calificacion')
        comentario_value = request.form.get('comentario')

        if calificacion_usuario:
            nueva_calif = calificacion_usuario
            # Opcional: si quieres permitir cambiar estrellas, descomenta la siguiente línea:
            # nueva_calif.calificacion = int(calif_value) 
        else:
            if not calif_value:
                return redirect(url_for('ver_receta', idReceta=idReceta))
            nueva_calif = Calificacion()
            nueva_calif.idUsuario = current_user.idUsuario
            nueva_calif.idReceta = idReceta
            nueva_calif.calificacion = int(calif_value)
        
        if comentario_value:
            nueva_calif.comentario = comentario_value
        else:
            nueva_calif.comentario = "Sin comentario"

        nueva_calif.agregar_o_actualizar()
        return redirect(url_for('ver_receta', idReceta=idReceta))
        
    return render_template('ver-receta.html', receta=r, promedio=promedio, calificacion_usuario=calificacion_usuario)

@app.route('/admin/comentario/eliminar/<int:idCalificacion>', methods=['POST'])
@login_required
def eliminar_comentario_admin(idCalificacion):
    
    
    calif_dao = Calificacion()
    c = calif_dao.consultaIndividual(idCalificacion)

    if not current_user.is_authenticated and ( current_user.is_admin() or c.idUsuario==current_user.idUsuario):
        abort(403)

    if c:
        idReceta = c.idReceta
        calif_dao.eliminar(idCalificacion)
        flash('Comentario eliminado por administración.', 'info')
        return redirect(url_for('ver_receta', idReceta=idReceta))
    
    return redirect(url_for('index'))

@app.route('/admin/comentario/editar/<int:idCalificacion>', methods=['GET', 'POST'])
@login_required
def editar_comentario_admin(idCalificacion):
    
        
    c = Calificacion().consultaIndividual(idCalificacion)
    if not c:
        abort(404)

    if not current_user.is_authenticated and ( current_user.is_admin() or c.idUsuario==current_user.idUsuario):
        abort(403)

    if request.method == 'POST':
        c.comentario = request.form['comentario']
        # c.calificacion = int(request.form['calificacion']) 
        c.editar()
        return redirect(url_for('ver_receta', idReceta=c.idReceta))

    return render_template('editar-comentario.html', comentario=c)

@app.route('/admin/sugerencias')
@login_required
def ver_sugerencias_admin():
    if not current_user.is_admin():
        abort(403)
    
    lista_sugerencias = Sugerencia().consultaGeneral()
    return render_template('ver-sugerencias.html', sugerencias=lista_sugerencias)

@app.route('/admin/sugerencias/eliminar/<int:idSugerencia>', methods=['POST'])
@login_required
def eliminar_sugerencia(idSugerencia):
    if not current_user.is_admin():
        abort(403)
        
    Sugerencia().eliminar(idSugerencia)
    flash('Sugerencia eliminada correctamente.', 'success')
    return redirect(url_for('ver_sugerencias_admin'))

@app.route('/sugerencias', methods=['GET', 'POST'])
def sugerencias():
    if request.method == 'POST':
        email = request.form['email']
        mensaje = request.form['mensaje']
        
        nueva_sugerencia = Sugerencia()
        nueva_sugerencia.email = email
        nueva_sugerencia.mensaje = mensaje
        
        nueva_sugerencia.agregar()
        
        return redirect(url_for('sugerencias'))
        
    return render_template('sugerencias.html')

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/categorias', methods=['GET', 'POST'])
def ver_categorias():
    cat = Categoria().consultaGeneral()
    rec = Receta().consultaGeneral()
    
    idCategoria = 0
    dificultad = '0'

    if request.method == 'POST':
        idCategoria = request.form.get('categoria', '0')
        dificultad = request.form.get('dificultad', '0')
        
        query = Receta.query
        
        if idCategoria != '0':
            query = query.filter(Receta.idCategoria == idCategoria)
            
        if dificultad != '0':
            query = query.filter(Receta.dificultad == dificultad)
        
        rec = query.all()
        
    return render_template('categorias.html', categorias=cat, recetas=rec, categoriaSel = int(idCategoria), dificultadSel = dificultad, calif=Calificacion)
    
@app.route('/nueva_categoria', methods=['GET', 'POST'])
@login_required
def nueva_categoria():
    if not current_user.is_admin():
        abort(403)

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        
        nueva_cat = Categoria()
        nueva_cat.nombre = nombre
        nueva_cat.descripcion = descripcion
            
        nueva_cat.agregar()
        flash('Categoría agregada exitosamente', 'success')
        return redirect(url_for('admin_categorias'))
        
    return render_template('nueva-categoria.html')

@app.route('/categoria/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    if not current_user.is_admin():
        abort(403)
        
    cat = Categoria().consultaIndividual(id)
    if not cat:
        abort(404)

    if request.method == 'POST':
        cat.nombre = request.form['nombre']
        cat.descripcion = request.form['descripcion']
        
        cat.editar()
        flash('Categoría actualizada', 'success')
        return redirect(url_for('admin_categorias'))

    return render_template('editar-categoria.html', categoria=cat)

@app.route('/categoria/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_categoria(id):
    if not current_user.is_admin():
        abort(403)
        
    cat = Categoria().consultaIndividual(id)
    if cat:
        db.session.delete(cat)
        db.session.commit()
        flash('Categoría eliminada', 'success')
    
    return redirect(url_for('ver_categorias'))

@app.route('/admin/recetas')
@login_required
def admin_recetas():
    if not current_user.is_admin():
        abort(403)
    
    recetas = Receta().consultaGeneral()
    return render_template('admin-recetas.html', recetas=recetas, calif=Calificacion)

@app.route('/admin/categorias')
@login_required
def admin_categorias():
    if not current_user.is_admin():
        abort(403)
    
    categorias = Categoria().consultaGeneral()
    return render_template('admin-categorias.html', categorias=categorias)

@app.route('/buscar')
def buscar():
    query = request.args.get('q', '')
    
    categorias = Categoria().consultaGeneral()
    
    if query:
        recetas_encontradas = Receta.query.filter(
            or_(Receta.nombre.like(f'%{query}%'), Receta.descripcion.like(f'%{query}%'), Receta.ingredientes.like(f'%{query}%'))).all()
    else:
        recetas_encontradas = []

    return render_template('resultados-busqueda.html', recetas=recetas_encontradas, categorias=categorias,categoriaSel=0,dificultadSel='0',calif=Calificacion,busqueda=query)

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