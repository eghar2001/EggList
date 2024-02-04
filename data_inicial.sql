START TRANSACTION;

/*
Seleccionar BBDD del proyecto


*/

/*

Roles

*/



INSERT INTO `egglist`.`roles`
(`name`)
VALUES
('Usuario');

INSERT INTO `egglist`.`roles`
(`name`)
VALUES
('Admin');


/*
Roles en lista
*/


INSERT INTO `egglist`.`roles_en_lista`
(`name`)
VALUES
('Armador');

INSERT INTO `egglist`.`roles_en_lista`
(`name`)
VALUES
('Comprador');
/*

PROVINCIAS

*/



#PROV ID 1
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Buenos Aires');

#PROV ID 2
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('CABA');

#PROV ID 3
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Catamarca');

#PROV ID 4
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Chaco');

#PROV ID 5
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Chubut');

#PROV ID 6
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Córdoba');

#PROV ID 7
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Corrientes');

#PROV ID 8
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Entre Ríos');


#PROV ID 9
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Formosa');

#PROV ID 10
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Jujuy');

#PROV ID 11
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('La Pampa');

#PROV ID 12
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('La Rioja');

#PROV ID 13
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Mendoza');

#PROV ID 14
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Misiones');

#PROV ID 15
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Neuquén');

#PROV ID 16
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Río Negro');

#PROV ID 17
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Salta');

#PROV ID 18
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('San Juan');

#PROV ID 19
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('San Luis');

#PROV ID 20
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santa Cruz');

#PROV ID 21
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santa Fe');

#PROV ID 22
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Santiago del Estero');

#PROV ID 23
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Tierra del fuego');

#PROV ID 24
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Tucumán');

#PROV ID 25
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Antártida');

#PROV ID 26
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Islas Malvinas');

#PROV ID 27
INSERT INTO `egglist`.`provincias`
(`nombre`)
VALUES
('Uruguay');



















/* 
CIUDADES
*/



#Provincia de Santa Fe




#CAÑADA
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`)
VALUES
(2500,
'Cañada de Gomez',
21);


#CHABÁS
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`)
VALUES
(2173,
'Chabás',
21);

#ROSARIO
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`)
VALUES
(2000,
'Rosario',
21);


#VILLA CAÑÁS
INSERT INTO `egglist`.`ciudades`
(`cod_postal`,
`nombre`,
`id_provincia`)
VALUES
(2607,
'Villa Cañás',
21);











/*
Supermercados
*/


#Cañada
INSERT INTO `egglist`.`supermercados`
(
`nombre`,
`cod_postal`)
VALUES
('Super Ahorro (Chacabuco 747)',
2500);


#CHABÁS
INSERT INTO `egglist`.`supermercados`
(
`nombre`,
`cod_postal`)
VALUES
('El Solar Supermercado(Mitre 1679)',
2173);

#ROSARIO
INSERT INTO `egglist`.`supermercados`
(
`nombre`,
`cod_postal`)
VALUES
('Supermercado La Reina(San Martín 3419)',
2000);

INSERT INTO `egglist`.`supermercados`
(
`nombre`,
`cod_postal`)
VALUES
('Carrefour (27 feb 100)',
2000);


#VILLA CAÑAS
INSERT INTO `egglist`.`supermercados`usuarios
(
`nombre`,
`cod_postal`)
VALUES
('Supermercados Dia(299, calle 7)',
2607);


COMMIT;