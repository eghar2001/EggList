from typing import List

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from eggList import db
from eggList.listas.forms import CrearListaForm, EnSupermercadoForm
from eggList.models import ListaProductos, Producto, Usuario, RolLista, Compra, Supermercado, Ciudad, Provincia
from eggList.productos.forms import AgregarProductoForm, CarritoForm
from eggList.utils import send_email
from eggList.usuarios.logic import user_roles_required
from eggList.listas import logic as lista_logic
from eggList.compras import logic as compra_logic
listas = Blueprint('listas', __name__)


@listas.route("/lista/mis-listas")
@login_required
@user_roles_required("Usuario")
def mis_listas():
    listas = current_user.listas[::-1]
    listas_por_semana = []
    if listas:
        semana = listas[0].get_semana()
        listas_por_semana = [(semana,[])]
        index = 0
        for lista in listas:
            if lista.get_semana() == semana:
                listas_por_semana[index][1].append(lista)
            else:
                semana = lista.get_semana()
                listas_por_semana.append((semana,[lista]))
                index += 1


    return render_template("listas/mis_listas.html", listas_por_semana = listas_por_semana)




@listas.route("/lista/crear", methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def crear_lista():
    form = CrearListaForm()
    if form.validate_on_submit():
        usuarios = []
        if form.incluye_grupo_familiar.data and current_user.grupo_familiar:
            usuarios += current_user.grupo_familiar.integrantes
        else:
            usuarios.append(current_user)

        lista = ListaProductos(
            descripcion = form.descripcion.data,
            usuarios = usuarios,
            autor = current_user
        )
        lista_logic.crear_lista(lista)
        send_email(users = lista.usuarios, title = f"Se ha creado la lista {lista.descripcion}",
                   body = f"""Se ha creado la lista {lista.descripcion}             
                   
                   """)
        flash("Su lista se ha agregado correctamente","success")
        return redirect(url_for("listas.mis_listas"))
    return render_template("/listas/crear_lista_form.html", form = form)

@listas.route("/lista/<int:lista_id>")
@login_required
@user_roles_required("Usuario")
def lista(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)

    if not lista.usuario_valido(current_user):
        abort(403)
    compra_disponible = lista_logic.buscar_compra_disponible(lista)
    if lista_logic.user_has_list_role(lista,"Comprador") and compra_disponible:
        form_carrito = CarritoForm()
        productos_disponibles = list(filter(lambda producto: not producto.id_compra, lista.productos))
        productos_en_carrito = []
        productos_fuera_de_carrito = []
        for producto in productos_disponibles:
            if producto.esta_en_carrito:
                productos_en_carrito.append(producto)
            else:
                productos_fuera_de_carrito.append(producto)
        total = lista.get_total()
        return render_template("listas/lista_comprador.html", lista=lista,
                               productos_en_carrito=productos_en_carrito,
                               productos_fuera_de_carrito=productos_fuera_de_carrito,
                               form_carrito=form_carrito, total=total, compra = compra_disponible)
    else:
        form = EnSupermercadoForm()

        ciudad_user:Ciudad = Ciudad.query.filter(Ciudad.id == current_user.id_ciudad).first()
        supermercados:List[Supermercado] = Supermercado.query.filter(Supermercado.id_ciudad == ciudad_user.id).all()
        form.supermercado.choices = [(super.id, super.nombre) for super in supermercados]
        lista.productos.sort(key = lambda producto: bool(producto.id_compra))
        return render_template("listas/lista_armador.html",lista = lista,
                               supermercados = supermercados, form_super = form,
                               ciudad_user=ciudad_user, compra = compra_disponible)




@listas.route("/lista/<int:lista_id>/en_supermercado/<int:supermercado_id>", methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def en_supermercado(lista_id, supermercado_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    supermercado = Supermercado.query.get_or_404(supermercado_id)
    lista_logic.en_supermercado(lista, supermercado)
    return redirect(url_for("listas.lista",lista_id = lista.id))


@listas.route("/lista/<int:lista_id>/agregar", methods = ["GET","POST"])
@login_required
@user_roles_required("Usuario")
def agregar_producto(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    form = AgregarProductoForm()
    if form.validate_on_submit():

        producto = Producto(descripcion=form.descripcion.data,
                            cantidad=form.cantidad.data if form.cantidad.data != 0 else None,
                            autor = current_user)
        lista_logic.agregar_producto(lista,producto)
        flash(f'Se agregó correctamente el producto {producto.descripcion} a tu lista!', "success")
        return redirect(url_for('listas.lista', lista_id = lista.id))

    return render_template('productos/agregar_producto_form.html', form = form, lista_id = lista.id)


@listas.route("/lista/<int:lista_id>/comprar")
@login_required
@user_roles_required("Usuario")
def comprar(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    compra_disponible = lista_logic.buscar_compra_disponible(lista)
    if lista_logic.user_has_list_role(lista, "Comprador") and compra_disponible:
        productos_comprados = list(filter(lambda producto: producto.esta_en_carrito and not producto.id_compra, lista.productos))
        if not productos_comprados:
            flash("No hay productos en tu carrito","primary")
            return redirect(url_for("listas.lista", lista_id = lista.id))
        lista_logic.actualizar_rol(lista, "Armador", commit=False)
        compra_logic.comprar(compra_disponible, productos_comprados, commit=True)



        return redirect(url_for("listas.lista", lista_id = lista.id))

@listas.route("/listas/<int:lista_id>/salir_del_super")
@login_required
@user_roles_required("Usuario")
def salir_del_super(lista_id):
    lista = ListaProductos.query.get_or_404(lista_id)
    if current_user in lista.usuarios:
        lista_logic.actualizar_rol(lista, "Armador", commit = True)
        if  (not any([lista_logic.user_has_list_role(lista=lista,rol_lista_str= "Comprador",user= user)
                and user != current_user for user in lista.usuarios])):
            lista_logic.salir_del_super(lista)
        return redirect(url_for('listas.lista', lista_id = lista.id))

    else:
        abort(403)