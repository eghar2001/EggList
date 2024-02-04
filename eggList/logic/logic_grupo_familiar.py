from flask import url_for
from flask_login import current_user
from werkzeug.datastructures.file_storage import FileStorage

from eggList import db
from eggList.data import data_grupo_familiar, data_usuario
from eggList.logic import logic_usuario
from eggList.logic.logic_usuario import UsuarioNoEncontradoException
from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario
from eggList.utils import save_family_picture, send_email


class UsuarioEnGrupoException(Exception):
    pass
class GrupoNoEncontradoException(Exception):
    pass


def crear_grupo(grupo:GrupoFamiliar, imagen: FileStorage):
    # Validamos que el nombre no se repita
    grupo_existente = data_grupo_familiar.get_grupo_familiar(nombre = grupo.nombre_familia)
    if grupo_existente:
        raise


    #Si se ingresó una imagen, se guarda y se le asigna el nombre a la propiedadn imagen_grupo del grupo familiar
    #Caso contrario, se le asigna el default desde la base de datos
    imagen_nombre = None
    if imagen:
        imagen_nombre = save_family_picture(imagen)
    grupo.imagen_grupo = imagen_nombre



    db.session.add(grupo)

    db.session.rollback()
    #db.session.commit()


def get_grupo_by_nombre(nombre: str):
    return data_grupo_familiar.get_grupo_familiar(nombre = nombre)


def invitar_usuario(user:Usuario):
    usuario_a_invitar = data_usuario.get_user(email = user.email)
    if not usuario_a_invitar or not usuario_a_invitar.esta_confirmado():
        raise UsuarioNoEncontradoException
    if current_user.es_familiar_de(usuario_a_invitar):
        raise UsuarioEnGrupoException
    send_email([usuario_a_invitar],
               title=f"'{current_user.nombre} {current_user.apellido}' te invitado de su grupo familiar",
               body=f"""Si desea unirse al grupo familiar '{current_user.grupo_familiar.nombre_familia}', dirijase al siguiente link
    {url_for('grupos_familiares.confirmar_usuario', grupo_familiar=current_user.grupo_familiar.nombre_familia, confirm_token=usuario_a_invitar.get_id_token(), _external=True)}                   

    Caso contrario, ignore este email
    """)

def agregar_integrante(grupo:GrupoFamiliar, token:str):
    user = logic_usuario.verify_id_token(token)
    grupo = data_grupo_familiar.get_grupo_familiar(nombre=grupo.nombre_familia)
    if  not grupo:
        raise GrupoNoEncontradoException("El ingresado no se encontro")
    if not user:
        raise UsuarioNoEncontradoException("El usuario ingresado no se encontro")
    if user.grupo_familiar:
        raise UsuarioEnGrupoException("El usuario ingresado ya posee un grupo familiar")
    grupo.agregar_integrante(user)
    db.session.commit()