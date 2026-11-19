"""CRUD de la tabla operaciones (FK a vehiculos, clientes y asesores).

Cada operación es una Compra (el concesionario le compra el vehículo al cliente)
o una Venta (el concesionario se lo vende al cliente).
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

import validators as v
from db import DatabaseError, error_message, execute, query

bp = Blueprint("operaciones", __name__, url_prefix="/operaciones")

TIPOS = ["Compra", "Venta"]
FORMAS_PAGO = ["Contado", "Crédito", "Permuta"]


def _leer_formulario(form):
    errores = []
    datos = {
        "fecha": v.fecha(form, "fecha", "Fecha", errores),
        "tipo_operacion": v.opcion(form, "tipo_operacion", "Tipo de operación", errores, TIPOS),
        "id_vehiculo": v.entero(form, "id_vehiculo", "Vehículo", errores, minimo=1),
        "id_cliente": v.entero(form, "id_cliente", "Cliente", errores, minimo=1),
        "id_asesor": v.entero(form, "id_asesor", "Asesor", errores, minimo=1),
        "valor": v.decimal(form, "valor", "Valor", errores, mayor_que=0),
        "forma_pago": v.opcion(form, "forma_pago", "Forma de pago", errores, FORMAS_PAGO),
        "observaciones": v.texto(form, "observaciones", "Observaciones", errores,
                                 obligatorio=False, max_len=200),
    }
    return datos, errores


def _render_form(item, titulo):
    return render_template(
        "operaciones/form.html", item=item, titulo=titulo, tipos=TIPOS, formas_pago=FORMAS_PAGO,
        vehiculos=query("""SELECT ve.id_vehiculo, ve.placa, ve.linea, ve.anio, ve.precio_venta,
                                  ve.estado, m.nombre_marca
                             FROM vehiculos ve
                             JOIN marcas m ON m.id_marca = ve.id_marca
                            ORDER BY m.nombre_marca, ve.linea"""),
        clientes=query("SELECT id_cliente, nombre_cliente, documento FROM clientes "
                       "ORDER BY nombre_cliente"),
        asesores=query("SELECT id_asesor, nombre_asesor FROM asesores ORDER BY nombre_asesor"),
    )


@bp.route("/")
def listar():
    items = query("""
        SELECT o.*, c.nombre_cliente, a.nombre_asesor,
               m.nombre_marca || ' ' || ve.linea AS vehiculo, ve.placa
          FROM operaciones o
          JOIN vehiculos ve ON ve.id_vehiculo = o.id_vehiculo
          JOIN marcas    m  ON m.id_marca     = ve.id_marca
          JOIN clientes  c  ON c.id_cliente   = o.id_cliente
          JOIN asesores  a  ON a.id_asesor    = o.id_asesor
         ORDER BY o.fecha DESC, o.id_operacion DESC
    """)
    return render_template("operaciones/list.html", items=items)


@bp.route("/nuevo", methods=["GET", "POST"])
def crear():
    item = {"tipo_operacion": "Venta", "forma_pago": "Contado"}
    if request.method == "POST":
        item = request.form.to_dict()
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""INSERT INTO operaciones (fecha, tipo_operacion, id_vehiculo, id_cliente,
                                                    id_asesor, valor, forma_pago, observaciones)
                           VALUES (%(fecha)s, %(tipo_operacion)s, %(id_vehiculo)s, %(id_cliente)s,
                                   %(id_asesor)s, %(valor)s, %(forma_pago)s, %(observaciones)s)""",
                        datos)
                flash("Operación registrada correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return _render_form(item, "Nueva operación")


@bp.route("/<int:id>/editar", methods=["GET", "POST"])
def editar(id):
    item = query("SELECT * FROM operaciones WHERE id_operacion = %s", (id,), one=True)
    if item is None:
        abort(404)
    if request.method == "POST":
        item = {**item, **request.form.to_dict()}
        datos, errores = _leer_formulario(request.form)
        if not errores:
            try:
                execute("""UPDATE operaciones
                              SET fecha          = %(fecha)s,
                                  tipo_operacion = %(tipo_operacion)s,
                                  id_vehiculo    = %(id_vehiculo)s,
                                  id_cliente     = %(id_cliente)s,
                                  id_asesor      = %(id_asesor)s,
                                  valor          = %(valor)s,
                                  forma_pago     = %(forma_pago)s,
                                  observaciones  = %(observaciones)s
                            WHERE id_operacion = %(id)s""",
                        {**datos, "id": id})
                flash("Operación actualizada correctamente.", "success")
                return redirect(url_for(".listar"))
            except DatabaseError as exc:
                errores.append(error_message(exc))
        for e in errores:
            flash(e, "danger")
    return _render_form(item, "Editar operación")


@bp.route("/<int:id>/eliminar", methods=["POST"])
def eliminar(id):
    try:
        if execute("DELETE FROM operaciones WHERE id_operacion = %s", (id,)):
            flash("Operación eliminada.", "success")
        else:
            flash("La operación no existe.", "warning")
    except DatabaseError as exc:
        flash(error_message(exc), "danger")
    return redirect(url_for(".listar"))
