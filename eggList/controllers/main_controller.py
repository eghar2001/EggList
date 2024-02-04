from flask import Blueprint, render_template
from flask_login import current_user
from eggList.logic import logic_provincia
from eggList.logic import logic_usuario
main = Blueprint('main',__name__)


@main.route("/home")
@main.route("/")
def home():
    if current_user.is_authenticated:
        listas_semanales = logic_usuario.get_listas_semanales()
        ultimas_3_compras = logic_usuario.get_ultimas_n_compras()
        provincias = logic_provincia.find_all()
        return render_template('main/home.html',listas_semanales = listas_semanales, ultimas_compras = ultimas_3_compras,
                               provincias = provincias)
    else:
        return render_template('main/home.html')
