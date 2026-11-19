"""Punto de entrada de la aplicación CRUD de compra y venta de vehículos."""
import psycopg2
from flask import Flask, flash, redirect, render_template, request, session, url_for

import db
from config import Config
from routes.asesores import bp as asesores_bp
from routes.auth import bp as auth_bp
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


# Colores con los que se pintan las ilustraciones de los vehículos
COLORES = {
    "Blanco": "#f4f5f7", "Negro": "#23272b", "Gris": "#8a9099", "Plata": "#c3c8ce",
    "Rojo": "#c0392b", "Azul": "#2c6db3", "Verde": "#2e8b57", "Amarillo": "#f1c40f",
    "Naranja": "#e67e22", "Café": "#7b4a2a", "Vinotinto": "#6d1a2a", "Beige": "#d8c8a8",
}


def color_hex(nombre):
    """Filtro Jinja: 'rojo' -> '#c0392b'. Si el color no está en la lista, usa gris."""
    return COLORES.get((nombre or "").strip().capitalize(), "#6c757d")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    app.add_template_filter(formato_pesos, "pesos")
    app.add_template_filter(formato_miles, "miles")
    app.add_template_filter(color_hex, "color_hex")
    app.add_template_global(COLORES, "colores")

    for bp in (auth_bp, marcas_bp, vehiculos_bp, clientes_bp, asesores_bp, operaciones_bp):
        app.register_blueprint(bp)

    # Páginas que cualquier visitante puede ver sin iniciar sesión
    PUBLICAS = {"catalogo", "auth.login", "static"}

    @app.before_request
    def exigir_sesion():
        """Todo lo que no sea público requiere haber iniciado sesión como administrador."""
        if request.endpoint is None or request.endpoint in PUBLICAS or session.get("admin"):
            return None
        flash("Inicia sesión para administrar los datos.", "warning")
        destino = request.full_path if request.method == "GET" else None
        return redirect(url_for("auth.login", next=destino))

    @app.route("/")
    def catalogo():
        """Catálogo público: solo vehículos disponibles o reservados, sin botones de edición."""
        vehiculos = db.query("""
            SELECT ve.*, m.nombre_marca
              FROM vehiculos ve
              JOIN marcas m ON m.id_marca = ve.id_marca
             WHERE ve.estado IN ('Disponible', 'Reservado')
             ORDER BY ve.estado, ve.precio_venta DESC
        """)
        return render_template("catalogo.html", vehiculos=vehiculos)

    @app.route("/panel")
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
        # Totales por mes para el gráfico de compras vs. ventas
        por_mes = db.query("""
            SELECT to_char(date_trunc('month', fecha), 'YYYY-MM') AS mes,
                   COALESCE(SUM(valor) FILTER (WHERE tipo_operacion = 'Compra'), 0) AS compras,
                   COALESCE(SUM(valor) FILTER (WHERE tipo_operacion = 'Venta'), 0)  AS ventas
              FROM operaciones
             GROUP BY 1
             ORDER BY 1
        """)
        grafico = {
            "meses": [f["mes"] for f in por_mes],
            "compras": [float(f["compras"]) for f in por_mes],
            "ventas": [float(f["ventas"]) for f in por_mes],
        }
        ultimas = db.query("""
            SELECT o.id_operacion, o.fecha, o.tipo_operacion, o.valor, c.nombre_cliente,
                   m.nombre_marca || ' ' || ve.linea AS vehiculo, ve.tipo, ve.color, ve.foto
              FROM operaciones o
              JOIN vehiculos ve ON ve.id_vehiculo = o.id_vehiculo
              JOIN marcas    m  ON m.id_marca     = ve.id_marca
              JOIN clientes  c  ON c.id_cliente   = o.id_cliente
             ORDER BY o.fecha DESC, o.id_operacion DESC
             LIMIT 5
        """)
        return render_template("index.html", c=conteos, grafico=grafico, ultimas=ultimas)

    @app.errorhandler(psycopg2.OperationalError)
    def error_conexion(exc):
        return render_template("error_db.html", error=str(exc)), 500

    @app.errorhandler(404)
    def no_encontrado(exc):
        return render_template("404.html"), 404

    @app.errorhandler(413)
    def archivo_muy_grande(exc):
        flash("La foto es demasiado grande: el máximo es 5 MB.", "danger")
        return redirect(request.referrer or url_for("vehiculos.listar"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
