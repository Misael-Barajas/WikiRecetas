from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, DateTime, BLOB, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    idUsuario = Column(Integer, primary_key=True)
    fotoUsuario = Column(BLOB)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    nombreUsuario = Column(String(50), unique=True, nullable=False)
    rol = Column(String(50), nullable=False, default='Usuario')
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(20), nullable=False)
    password = Column(String(255), nullable=False)
    nombre_apellido = Column(String(255), nullable=False)
    
    @property

    def __set_password(self, password):
        self.password = generate_password_hash(password)

    def validarPassword(self, password):
        return check_password_hash(self.password, password)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        usuario_existente = Usuario.query.get(self.idUsuario)
        if usuario_existente:
            db.session.merge(self)
            db.session.commit()
            return True
        return False
    
    def eliminar(self, id):
        u = self.consultaIndividual(id)
        db.session.delete(u)
        db.session.commit()

    def consultaIndividual(self, id):
        return Usuario.query.get(id)

    def validar(self, email, password):
        usuario = Usuario.query.filter(Usuario.email == email).first()
        if usuario is not None and usuario.validarPassword(password):
            return usuario
        else:
            return None
    
    def get_id(self):
        return self.idUsuario
    
    def is_authenticated(self):
        return True
    
    def consultarImagen(self,id):
        return self.consultaIndividual(id).fotoUsuario
    
    def is_admin(self):
        if self.rol=='Admin':
            return True
        else:
            return False


class Categoria(db.Model):
    __tablename__ = 'categoria'
    idCategoria = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(200), nullable=True)

    def consultaGeneral(self):
        return self.query.all()

    def consultaIndividual(self, id):
        return Categoria.query.get(id)
    
    def agregar(self):
        db.session.add(self)
        db.session.commit()
        
    def editar(self):
        db.session.merge(self)
        db.session.commit()

class Receta(db.Model):
    __tablename__ = 'receta'
    idReceta = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    dificultad = Column(String(50), nullable=False) 
    descripcion = Column(String(200), nullable=False)
    ingredientes = Column(String(500), nullable=False)
    preparacion = Column(String(1000), nullable=False)
    imagen = Column(BLOB)
    
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    idCategoria = Column(Integer, ForeignKey('categoria.idCategoria'), nullable=False)
    
    usuario = relationship('Usuario', backref='recetas')
    categoria = relationship('Categoria', backref='recetas')
    
    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def consultaGeneral(self):
        return self.query.all()
    
    def consultaIndividual(self, id):
        return Receta.query.get(id)

    def editar(self, idReceta):
        receta_existente = Receta.query.get(idReceta)
        if receta_existente:
            db.session.merge(self)
            db.session.commit()
            return True
        return False

    def eliminar(self, id):
        r = self.consultaIndividual(id)
        if r:
            Calificacion.query.filter_by(idReceta=id).delete()
            
            db.session.delete(r)
            db.session.commit()
            
    def consultarImagen(self,id):
        return self.consultaIndividual(id).imagen
    
    def consultarProductosPorCategoria(idCategoria):
        return Receta.query.filter_by(idCategoria=idCategoria).all()

class Calificacion(db.Model):
    __tablename__ = 'calificacion'
    idCalificacion = Column(Integer, primary_key=True) 
    calificacion = Column(Integer, nullable=False) 
    comentario = Column(String(1000), nullable=True)
    idUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'), nullable=False)
    idReceta = Column(Integer, ForeignKey('receta.idReceta'), nullable=False)
    usuario = relationship('Usuario', backref='calificaciones')
    receta = relationship('Receta', backref='calificaciones')
    
    def agregar(self):
        db.session.add(self)
        db.session.commit()
        
    @staticmethod
    def obtener_promedio(idReceta):
        from sqlalchemy import func
        promedio = db.session.query(func.avg(Calificacion.calificacion)).filter(Calificacion.idReceta == idReceta).scalar()
        if promedio is None:
            return 0.0
        return round(float(promedio), 1)
    
    def agregar_o_actualizar(self):
        calif_existente = Calificacion.query.filter_by(idUsuario=self.idUsuario, idReceta=self.idReceta).first()
        if calif_existente:
            calif_existente.calificacion = self.calificacion
        else:
            db.session.add(self)
        db.session.commit()
        
    def consultaIndividual(self, id):
        return Calificacion.query.get(id)

    def editar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        c = self.consultaIndividual(id)
        if c:
            db.session.delete(c)
            db.session.commit()

        
class Sugerencia(db.Model):
    __tablename__ = 'sugerencias'
    idSugerencia = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    mensaje = Column(String(1000), nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.now)

    def agregar(self):
        db.session.add(self)
        db.session.commit()
        
    def consultaGeneral(self):
        return self.query.order_by(Sugerencia.fecha.desc()).all()

    def consultaIndividual(self, id):
        return Sugerencia.query.get(id)

    def eliminar(self, id):
        s = self.consultaIndividual(id)
        if s:
            db.session.delete(s)
            db.session.commit()