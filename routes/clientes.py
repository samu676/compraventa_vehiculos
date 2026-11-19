"""CRUD de la tabla clientes."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("clientes", __name__, url_prefix="/clientes")


def _leer_formulario(form):
    errores = []
    datos = {
        "documento": v.patron(form, "documento", "Documento", errores, r"[0-9]{6,15}",
                              "debe tener solo números (entre 6 y 15 dígitos)."),
        "nombre_cliente": v.texto(form, "nombre_cliente", "Nombre", errores, max_len=100),
        "telefono": v.patron(form, "telefono", "Teléfono", errores, r"[0-9]{7,15}",
                             "debe tener solo números (entre 7 y 15 dígitos)."),
        "email": v.email(form, "email", "Email", errores),
        "ciudad": v.texto(form, "ciudad", "Ciudad", errores, max_len=60),
    }
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT cl.*,
               COUNT(o.id_operacion) FILTER (WHERE o.tipo_operacion = 'Compra') AS num_vendidos,
               COUNT(o.id_operacion) FILTER (WHERE o.tipo_operacion = 'Venta')  AS num_comprados
          FROM clientes cl
          LEFT JOIN operaciones o ON o.id_cliente = cl.id_cliente
         GROUP BY cl.id_cliente
         ORDER BY cl.id_cliente
    """)
    return render_template("clientes/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO clientes (documento, nombre_cliente, telefono, email, ciudad)
                           VALUES (%(documento)s, %(nombre_cliente)s, %(telefono)s,
                                   %(email)s, %(ciudad)s)""",
                        datos)
                flash("Cliente creado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("clientes/form.html", item=item, titulo="Nuevo cliente")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM clientes WHERE id_cliente = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE clientes
                              SET documento      = %(documento)s,
                                  nombre_cliente = %(nombre_cliente)s,
                                  telefono       = %(telefono)s,
                                  email          = %(email)s,
                                  ciudad         = %(ciudad)s
                            WHERE id_cliente = %(id)s""",
                        {**datos, "id": id})
                flash("Cliente actualizado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("clientes/form.html", item=item, titulo="Editar cliente")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM clientes WHERE id_cliente = %s", (id,)):
            flash("Cliente eliminado.", "success")
        else:
            flash("El cliente no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for(".listar"))
