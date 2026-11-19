"""CRUD de la tabla marcas."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("marcas", __name__, url_prefix="/marcas")


def _leer_formulario(form):
    errores = []
    datos = {
        "nombre_marca": v.texto(form, "nombre_marca", "Marca", errores, max_len=50),
        "pais_origen": v.texto(form, "pais_origen", "País de origen", errores, max_len=50),
    }
    return datos, errores


@bp.route("/")
def listar():
    items = query("""
        SELECT m.*, COUNT(ve.id_vehiculo) AS num_vehiculos
          FROM marcas m
          LEFT JOIN vehiculos ve ON ve.id_marca = m.id_marca
         GROUP BY m.id_marca
         ORDER BY m.nombre_marca
    """)
    return render_template("marcas/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO marcas (nombre_marca, pais_origen)
                           VALUES (%(nombre_marca)s, %(pais_origen)s)""", datos)
                flash("Marca creada correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("marcas/form.html", item=item, titulo="Nueva marca")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM marcas WHERE id_marca = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE marcas
                              SET nombre_marca = %(nombre_marca)s,
                                  pais_origen  = %(pais_origen)s
                            WHERE id_marca = %(id)s""",
                        {**datos, "id": id})
                flash("Marca actualizada correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return render_template("marcas/form.html", item=item, titulo="Editar marca")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM marcas WHERE id_marca = %s", (id,)):
            flash("Marca eliminada.", "success")
        else:
            flash("La marca no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for(".listar"))
