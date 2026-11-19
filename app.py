"""Punto de entrada de la aplicación CRUD de compra y venta de vehículos."""
import psycopg2
from flask import Flask, render_template

import db
from config import Config
from routes.asesores import bp as asesores_bp
from routes.clientes import bp as clientes_bp
from routes.marcas import bp as marcas_bp
from routes.operaciones import bp as operaciones_bp
from routes.vehiculos import bp as vehiculos_bp


def formato_pesos(valor):
    """Filtro Jinja: 58900000 -> $ 58.900.000"""
    if valor is None:
        return ""
    return "$ " + f"{float(valor):,.0f}".replace(",", ".")


def formato_miles(valor):
    """Filtro Jinja: 38000 -> 38.000"""
    if valor is None:
        return ""
    return f"{int(valor):,}".replace(",", ".")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.add_template_filter(formato_pesos, "pesos")
    app.add_template_filter(formato_miles, "miles")

    for bp in (marcas_bp, vehiculos_bp, clientes_bp, asesores_bp, operaciones_bp):
        app.register_blueprint(bp)

    @app.route("/")
    def inicio():
        conteos = db.query("""
            SELECT (SELECT COUNT(*) FROM marcas)      AS marcas,
                   (SELECT COUNT(*) FROM vehiculos)   AS vehiculos,
                   (SELECT COUNT(*) FROM clientes)    AS clientes,
                   (SELECT COUNT(*) FROM asesores)    AS asesores,
                   (SELECT COUNT(*) FROM operaciones) AS operaciones,
                   (SELECT COUNT(*) FROM vehiculos WHERE estado = 'Disponible') AS disponibles,
                   (SELECT COALESCE(SUM(valor), 0) FROM operaciones
                     WHERE tipo_operacion = 'Compra') AS total_compras,
                   (SELECT COALESCE(SUM(valor), 0) FROM operaciones
                     WHERE tipo_operacion = 'Venta')  AS total_ventas
        """, one=True)
        return render_template("index.html", c=conteos)

    @app.errorhandler(psycopg2.OperationalError)
    def error_conexion(exc):
        return render_template("error_db.html", error=str(exc)), 500

    @app.errorhandler(404)
    def no_encontrado(exc):
        return render_template("404.html"), 404

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
