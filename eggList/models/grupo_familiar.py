from flask import url_for

from eggList import db
from eggList.models.usuario import Usuario


class GrupoFamiliar(db.Model):
    """
    Clase que representa un grupo familiar dentro del programa
    Es decir, un conjunto de usuarios. Su mayor utilidad es para compartirse las listas
    """
    __tablename__ = "grupos_familiares"
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    nombre_familia = db.Column(db.String(50), nullable=False, unique=True)
    imagen_grupo = db.Column(db.String(20), nullable=  False, default = "default.jpg")
    integrantes = db.relationship('Usuario', back_populates="grupo_familiar")

    def agregar_integrante(self, nuevo_integrante):
        if isinstance(nuevo_integrante, Usuario):
            self.integrantes.append(nuevo_integrante)

    def get_img_url(self):
        return url_for('static',filename = "grupo_familiar_pics/"+self.imagen_grupo)
