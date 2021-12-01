CREATE DATABASE IF NOT EXISTS `sistema`;
USE `sistema`;
CREATE TABLE IF NOT EXISTS empleados (
    id int NOT NULL AUTO_INCREMENT,
    nombre varchar(255),
    correo varchar(255),
    foto varchar(5000),
    PRIMARY KEY (id)
);

--INSERT INTO empleados (id, nombre,correo,foto) VALUES(NULL, 'Camilo','camibello@gmail.com','foto.jpg');

-- SELECT * FROM empleados;