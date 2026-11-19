"""CRUD de la tabla asesores."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("asesores", __name__, url_prefix="/asesores")


def _leer_formulario(form):
    errores = []
    datos = {
        "nombre_asesor": v.texto(form, "nombre_asesor", "Nombre", errores, max_len=100),
        "telefono": v.patron(form, "telefono", "Teléfono", errores, r"[0-9]{7,15}",
                             "debe tener solo números (entre 7 y 15 dígitos)."),
        "email": v.email(form, "email", "Email", errores, obligatorio=True),
        "porcentaje_comision": v.decimal(form, "porcentaje_comision", "Comisión (%)", errores,
                                         minimo=0, maximo=10),
    }
    return datos, errores


@bp.route("/")
def listar():
    # La comisión se calcula (valor x porcentaje); no se guarda para no duplicar datos (3FN)
    items = query("""
        SELECT a.*,
               COUNT(o.id_operacion)        AS num_operaciones,
               COALESCE(SUM(o.valor), 0)    AS total_negociado,
               COALESCE(SUM(o.valor), 0) * a.porcentaje_comision / 100 AS comision
          FROM asesores a
          LEFT JOIN operaciones o ON o.id_asesor = a.id_asesor
         GROUP BY a.id_asesor
         ORDER BY a.id_asesor
    """)
    return render_template("asesores/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {"porcentaje_comision": 2}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO asesores (nombre_asesor, telefono, email, porcentaje_comision)
                           VALUES (%(nombre_asesor)s, %(telefono)s, %(email)s,
                                   %(porcentaje_comision)s)""",
                        datos)
                flash("Asesor creado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("asesores/form.html", item=item, titulo="Nuevo asesor")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM asesores WHERE id_asesor = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE asesores
                              SET nombre_asesor       = %(nombre_asesor)s,
                                  telefono            = %(telefono)s,
                                  email               = %(email)s,
                                  porcentaje_comision = %(porcentaje_comision)s
                            WHERE id_asesor = %(id)s""",
                        {**datos, "id": id})
                flash("Asesor actualizado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("asesores/form.html", item=item, titulo="Editar asesor")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM asesores WHERE id_asesor = %s", (id,)):
            flash("Asesor eliminado.", "success")
        else:
            flash("El asesor no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for(".listar"))
