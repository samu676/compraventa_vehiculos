"""CRUD de la tabla vehiculos (FK a marcas)."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

TIPOS = ["Automóvil", "SUV", "Camioneta", "Motocicleta"]
ESTADOS = ["Disponible", "Reservado", "Vendido"]
ANIO_MIN, ANIO_MAX = 1980, 2027


def _leer_formulario(form):
    errores = []
    datos = {
        "id_marca": v.entero(form, "id_marca", "Marca", errores, minimo=1),
        "linea": v.texto(form, "linea", "Línea / modelo", errores, max_len=60),
        "anio": v.entero(form, "anio", "Año", errores, minimo=ANIO_MIN, maximo=ANIO_MAX),
        # Placa colombiana: ABC123 para carros, ABC12D para motos
        "placa": v.patron(form, "placa", "Placa", errores, r"[A-Z]{3}[0-9]{2}[0-9A-Z]",
                          "debe tener el formato ABC123 (carro) o ABC12D (moto).",
                          mayusculas=True),
        "tipo": v.opcion(form, "tipo", "Tipo", errores, TIPOS),
        "color": v.texto(form, "color", "Color", errores, max_len=30),
        "kilometraje": v.entero(form, "kilometraje", "Kilometraje", errores, minimo=0),
        "precio_venta": v.decimal(form, "precio_venta", "Precio de venta", errores, mayor_que=0),
        "estado": v.opcion(form, "estado", "Estado", errores, ESTADOS),
    }
    return datos, errores


def _render_form(item, titulo):
    return render_template(
        "vehiculos/form.html", item=item, titulo=titulo, tipos=TIPOS, estados=ESTADOS,
        anio_min=ANIO_MIN, anio_max=ANIO_MAX,
        marcas=query("SELECT id_marca, nombre_marca FROM marcas ORDER BY nombre_marca"),
    )


@bp.route("/")
def listar():
    items = query("""
        SELECT ve.*, m.nombre_marca
          FROM vehiculos ve
          JOIN marcas m ON m.id_marca = ve.id_marca
         ORDER BY ve.id_vehiculo
    """)
    return render_template("vehiculos/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {"estado": "Disponible", "kilometraje": 0}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO vehiculos (id_marca, linea, anio, placa, tipo, color,
                                                  kilometraje, precio_venta, estado)
                           VALUES (%(id_marca)s, %(linea)s, %(anio)s, %(placa)s, %(tipo)s,
                                   %(color)s, %(kilometraje)s, %(precio_venta)s, %(estado)s)""",
                        datos)
                flash("Vehículo creado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return _render_form(item, "Nuevo vehículo")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM vehiculos WHERE id_vehiculo = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE vehiculos
                              SET id_marca     = %(id_marca)s,
                                  linea        = %(linea)s,
                                  anio         = %(anio)s,
                                  placa        = %(placa)s,
                                  tipo         = %(tipo)s,
                                  color        = %(color)s,
                                  kilometraje  = %(kilometraje)s,
                                  precio_venta = %(precio_venta)s,
                                  estado       = %(estado)s
                            WHERE id_vehiculo = %(id)s""",
                        {**datos, "id": id})
                flash("Vehículo actualizado correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return _render_form(item, "Editar vehículo")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM vehiculos WHERE id_vehiculo = %s", (id,)):
            flash("Vehículo eliminado.", "success")
        else:
            flash("El vehículo no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for(".listar"))
