create database WikiRecetas;
use WikiRecetas;

create table usuarios(
	idUsuario int auto_increment primary key not null,
    fotoUsuario blob,
    nombre varchar(50) not null,
    apellido varchar(50) not null,
    nombre_apellido varchar(255) not null,
    nombreUsuario varchar(50) not null,
    rol varchar(50) not null,
    email varchar(255) not null unique,
    telefono varchar(20) not null,
    password varchar(255) not null,
    check (email regexp '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    check (char_length(password) >= 8)
);

create table categoria(
	idCategoria int auto_increment primary key not null,
    nombre varchar(50) not null,
    descripcion varchar(200),
    imagen blob
);

create table receta(
	idReceta int auto_increment primary key not null,
    nombre varchar(50) not null,
    dificultad varchar(50) not null,
    descripcion varchar(200) not null,
    ingredientes varchar(500) not null,
    preparacion varchar(1000) not null,
    idUsuario int not null,
    idCategoria int not null,
	FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
    FOREIGN KEY (idCategoria) REFERENCES categoria(idCategoria)
);

create table imagenVideo(
	idImagenVideo int primary key auto_increment not null, 
	idReceta int not null,
    imagen blob not null,
    FOREIGN KEY (idReceta) REFERENCES receta(idReceta)
);

create table calificacion(
	idCalificacion int primary key auto_increment not null, 
	idReceta int not null,
    idUsuario int not null,
    calificacion int not null,
    comentario varchar(1000) not null,
    FOREIGN KEY (idReceta) REFERENCES receta(idReceta),
    FOREIGN KEY (idUsuario) REFERENCES usuarios(idUsuario),
    CHECK (calificacion BETWEEN 1 AND 5)
);

-- DEFAULT
alter table usuarios alter column rol set default 'Usuario';

-- INSERT INTO
insert into categoria(nombre, descripcion) values('Desayunos', 'Empieza tu día con energía con nuestras recetas fáciles y deliciosas.');
insert into categoria(nombre, descripcion) values('Comidas', 'Platos fuertes para toda la familia, con ingredientes sencillos.');
insert into categoria(nombre, descripcion) values('Postres', 'Dulces irresistibles para consentirte a cualquier hora del día.');
insert into categoria(nombre, descripcion) values('Bebidas', 'Refrescantes, frías o calientes, tenemos algo para todos los gustos.');


select * from usuarios;
select * from receta;
select * from imagenVideo;
