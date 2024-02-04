from flask import Blueprint, render_template, flash, redirect, url_for, abort, request
from flask_login import login_required, current_user
from eggList.forms.grupo_familiar_forms import GrupoFamiliarForm, AgregarUsuarioForm
from eggList.logic.logic_grupo_familiar import UsuarioEnGrupoException, GrupoNoEncontradoException
from eggList.models.grupo_familiar import GrupoFamiliar
from eggList.models.usuario import Usuario
from eggList.logic.logic_usuario import  user_roles_required, UsuarioNoEncontradoException
from eggList.logic import logic_grupo_familiar

grupos_familiares = Blueprint('grupos_familiares',__name__)

@grupos_familiares.route("/grupo_familiar/crear",methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def crear_grupo_familiar():
    form = GrupoFamiliarForm()
    if form.validate_on_submit():
        imagen = form.imagen.data

        grupo = GrupoFamiliar(
            nombre_familia = form.familia.data,
            integrantes = [current_user, ]
        )
        logic_grupo_familiar.crear_grupo(grupo,imagen)
        flash("Su grupo familiar se a creado correctamente", "success")
        return redirect(url_for('grupos_familiares.grupo_familiar'))

    return render_template('grupos_familiares/grupo_familiar_form.html', form=form)

@grupos_familiares.route("/grupo_familiar")
@login_required
@user_roles_required("Usuario")
def grupo_familiar():
    form = AgregarUsuarioForm()
    return render_template("grupos_familiares/grupo_familiar.html",form = form)

@grupos_familiares.route("/grupo_familiar/invitar_usuario",methods=["POST"])
@login_required
@user_roles_required("Usuario")
def invitar_usuario():
    form = AgregarUsuarioForm()

    if form.validate_on_submit():
        user = Usuario(email=form.email_usuario.data)
        try:
            logic_grupo_familiar.invitar_usuario(user)
        except UsuarioNoEncontradoException:
            flash("El mail ingresado no existe","danger")
            return redirect(url_for("grupos_familiares.grupo_familiar"))
        except UsuarioEnGrupoException:
            flash("El usuario ya se encuentra en el grupo", "info")
            return redirect(url_for("grupos_familiares.grupo_familiar"))


        flash(f"Se ha enviado la invitacion a '{user.email}'","primary")
        return redirect(url_for('grupos_familiares.grupo_familiar'))


@grupos_familiares.route("/grupo_familiar/<string:grupo_familiar>/confirmar_usuario/<confirm_token>")
@login_required
@user_roles_required("Usuario")
def confirmar_usuario(grupo_familiar, confirm_token):
    grupo = GrupoFamiliar(nombre_familia = grupo_familiar)
    try:
        logic_grupo_familiar.agregar_integrante(grupo,confirm_token)
    except UsuarioNoEncontradoException:
        flash("El usuario ingresado no se encontro", "danger")
        return redirect(url_for("grupo_familiar.grupo_familiar"))
    except GrupoNoEncontradoException:
        flash("El grupo buscado no existe","danger")
    except UsuarioEnGrupoException:
        flash("El usuario ingresado ya posee un grupo", "warning")
        return redirect(url_for("grupo_familiar.grupo_familiar"))
    flash(f"Te has unido satisfactoriamente al grupo familiar '{grupo.nombre_familia}'", "success")
    return redirect(url_for('usuarios.login'))


@grupos_familiares.route("/grupo_familiar/editar", methods=["GET","POST"])
@login_required
@user_roles_required("Usuario")
def editar():
    grupo = logic_grupo_familiar.get_grupo_by_nombre(current_user.grupo_familiar.nombre_familia)
    if not grupo:
        abort(404)
    form = GrupoFamiliarForm()
    form.familia.data = current_user.grupo_familiar.nombre_familia
    return render_template("/grupos_familiares/grupo_familiar_form.html", form=form,titulo = "Editar grupo familiar")


