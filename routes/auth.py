"""Inicio y cierre de sesión del administrador.

Solo hay un administrador: su usuario y clave están en el archivo .env
(ADMIN_USUARIO y ADMIN_CLAVE). Así el modelo de datos sigue teniendo 5 tablas.
"""
import hmac

from flask import (Blueprint, current_app, flash, redirect, render_template, request, session,
                   url_for)

bp = Blueprint("auth", __name__)


def _destino_seguro(destino):
    """Solo permite volver a rutas internas (evita redirigir a otros sitios)."""
    if destino and destino.startswith("/") and not destino.startswith("//"):
        return destino
    return url_for("inicio")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin"):
        return redirect(url_for("inicio"))
    if request.method == "POST":
        usuario = (request.form.get("usuario") or "").strip()
        clave = request.form.get("clave") or ""
        esperado = current_app.config["ADMIN_CLAVE"]
        # compare_digest compara en tiempo constante (buena práctica para claves)
        valido = (bool(esperado)
                  and hmac.compare_digest(usuario, current_app.config["ADMIN_USUARIO"])
                  and hmac.compare_digest(clave, esperado))
        if valido:
            session.clear()
            session["admin"] = usuario
            flash(f"Bienvenido, {usuario}.", "success")
            return redirect(_destino_seguro(request.args.get("next")))
        flash("Usuario o contraseña incorrectos.", "danger")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("catalogo"))
