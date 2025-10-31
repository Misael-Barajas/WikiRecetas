from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float, Date, BLOB, ForeignKey
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    fotoUsuario = Column(BLOB, nullable=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

class Receta(db.Model):
    __tablename__ = 'recetas'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500), nullable=True)
    ingredientes = Column(String(1000), nullable=False)
    preparacion = Column(String(2000), nullable=False)
    porciones = Column(Integer, nullable=True)
    categoria_id = Column(String(50), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship('Usuario', backref='recetas')

    def cosultaGeneral(self):
        return Receta.query.all()
    
    def conultaIndividual(self, id):
        return Receta.query.filter_by(id=id).first()
    
    def consultaAciva(self):
        return Receta.query.filter_by(estado='activo').all()

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
    
    def editar(self):
        db.session.merge(self)
        db.session.commit()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

class imajen_video(db.Model):
    __tablename__ = 'imajen_videos'
    id = Column(Integer, primary_key=True)
    imagen = Column(BLOB, nullable=False)  
    video = Column(String(200), nullable=False)
    receta_id = Column(Integer, ForeignKey('recetas.id'), nullable=False)
    receta = relationship('Receta', backref='imajen_videos')

    def agregar(self):
        db.session.add(self)
        db.session.commit()
    
    def eliminar(self):
        db.session.delete(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()

class calificacion(db.Model):
    __tablename__ = 'calificaciones'
    id = Column(Integer, primary_key=True)
    puntuacion = Column(Float, nullable=False)
    comentario = Column(String(500), nullable=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    receta_id = Column(Integer, ForeignKey('recetas.id'), nullable=False)
    usuario = relationship('Usuario', backref='calificaciones')
    receta = relationship('Receta', backref='calificaciones')

    def consultaGeneral(self):
        return calificacion.query.all()
    
    def agregar(self):
        db.session.add(self)
        db.session.commit()

    def editar(self):
        db.session.merge(self)
        db.session.commit()
    