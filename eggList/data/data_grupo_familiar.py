from typing import List

from flask_login import current_user

from eggList.models.grupo_familiar import GrupoFamiliar


def get_grupo_familiar(id_grupo:int = None, nombre:str = None):
    if id_grupo and nombre:
        raise ValueError("Solo se puede realizar la consulta por un parametro")
    grupo_familiar = None
    if id_grupo:
        grupo_familiar = GrupoFamiliar.query.get(id_grupo)
    elif nombre:
        grupo_familiar = GrupoFamiliar.query.filter(GrupoFamiliar.nombre_familia == nombre).first()
    return grupo_familiar
