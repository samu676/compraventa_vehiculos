"""Pruebas de punta a punta del CRUD contra la base compraventa_db real.

Cada prueba crea sus propios registros y los elimina al final,
así que los 10 registros originales de cada tabla no se modifican.

Ejecutar con:  python -m pytest -v
"""
import io
from pathlib import Path

import psycopg2
import pytest

from app import create_app
from config import Config

PREFIJO = "ZZ_TEST_"
TABLAS = ["marcas", "vehiculos", "clientes", "asesores", "operaciones"]
CLAVE_PRUEBA = "clave-de-prueba"


def _app():
    app = create_app()
    app.config["TESTING"] = True
    app.config["ADMIN_USUARIO"] = "admin"
    app.config["ADMIN_CLAVE"] = CLAVE_PRUEBA
    return app


@pytest.fixture()
def client():
    """Cliente con la sesión de administrador ya iniciada."""
    with _app().test_client() as c:
        with c.session_transaction() as s:
            s["admin"] = "admin"
        yield c


@pytest.fixture()
def anonimo():
    """Cliente de un visitante que no ha iniciado sesión."""
    with _app().test_client() as c:
        yield c


def sql(consulta, params=()):
    conn = psycopg2.connect(host=Config.DB_HOST, port=Config.DB_PORT, dbname=Config.DB_NAME,
                            user=Config.DB_USER, password=Config.DB_PASSWORD)
    with conn, conn.cursor() as cur:
        cur.execute(consulta, params)
        resultado = cur.fetchone() if cur.description else None
    conn.close()
    return resultado


def contar(tabla):
    assert tabla in TABLAS  # el nombre de la tabla nunca viene del usuario
    return sql(f"SELECT COUNT(*) FROM {tabla}")[0]


# ---------------------------------------------------------------- páginas

@pytest.mark.parametrize("ruta", ["/", "/panel"]
                         + [f"/{t}/" for t in TABLAS]
                         + [f"/{t}/nuevo" for t in TABLAS]
                         + [f"/{t}/1/editar" for t in TABLAS])
def test_paginas_cargan(client, ruta):
    assert client.get(ruta).status_code == 200


def test_registro_inexistente_da_404(client):
    assert client.get("/vehiculos/999999/editar").status_code == 404


def test_listados_muestran_nombres_y_no_ids(client):
    html = client.get("/vehiculos/").get_data(as_text=True)
    assert "Chevrolet" in html and "Onix LTZ" in html
    html = client.get("/operaciones/").get_data(as_text=True)
    assert "Daniela Castro Ibarra" in html and "Natalia Quintero Rivas" in html


# ---------------------------------------------------------------- marcas

def test_crud_marcas(client):
    antes = contar("marcas")
    r = client.post("/marcas/nuevo", data={"nombre_marca": PREFIJO + "Marca",
                                           "pais_origen": "Colombia"}, follow_redirects=True)
    assert "Marca creada" in r.get_data(as_text=True)
    id_ = sql("SELECT id_marca FROM marcas WHERE nombre_marca=%s", (PREFIJO + "Marca",))[0]

    r = client.post(f"/marcas/{id_}/editar", data={"nombre_marca": PREFIJO + "Marca2",
                                                   "pais_origen": "Italia"}, follow_redirects=True)
    assert "actualizada" in r.get_data(as_text=True)
    assert sql("SELECT nombre_marca, pais_origen FROM marcas WHERE id_marca=%s",
               (id_,)) == (PREFIJO + "Marca2", "Italia")

    r = client.post(f"/marcas/{id_}/eliminar", follow_redirects=True)
    assert "eliminada" in r.get_data(as_text=True)
    assert contar("marcas") == antes


def test_marca_duplicada_y_vacia(client):
    r = client.post("/marcas/nuevo", data={"nombre_marca": "Mazda", "pais_origen": "Japón"})
    assert "Ya existe un registro" in r.get_data(as_text=True)
    r = client.post("/marcas/nuevo", data={"nombre_marca": "  ", "pais_origen": ""})
    assert "«Marca» es obligatorio" in r.get_data(as_text=True)


def test_no_elimina_marca_con_vehiculos(client):
    r = client.post("/marcas/1/eliminar", follow_redirects=True)
    assert "relacionado" in r.get_data(as_text=True)
    assert sql("SELECT COUNT(*) FROM marcas WHERE id_marca=1")[0] == 1


# ---------------------------------------------------------------- vehiculos

VEHICULO = {"id_marca": "3", "linea": PREFIJO + "CX-30", "anio": "2023", "placa": "zzt901",
            "tipo": "SUV", "color": "Gris", "kilometraje": "5000", "precio_venta": "115000000",
            "estado": "Disponible"}


def test_crud_vehiculos(client):
    r = client.post("/vehiculos/nuevo", data=VEHICULO, follow_redirects=True)
    assert "Vehículo creado" in r.get_data(as_text=True)
    id_, placa = sql("SELECT id_vehiculo, placa FROM vehiculos WHERE linea=%s", (PREFIJO + "CX-30",))
    assert placa == "ZZT901"  # la placa se guarda en mayúsculas

    r = client.post(f"/vehiculos/{id_}/editar",
                    data={**VEHICULO, "precio_venta": "110000000", "estado": "Reservado"},
                    follow_redirects=True)
    assert "actualizado" in r.get_data(as_text=True)
    precio, estado = sql("SELECT precio_venta, estado FROM vehiculos WHERE id_vehiculo=%s", (id_,))
    assert float(precio) == 110000000 and estado == "Reservado"

    client.post(f"/vehiculos/{id_}/eliminar")
    assert sql("SELECT COUNT(*) FROM vehiculos WHERE id_vehiculo=%s", (id_,))[0] == 0


def test_vehiculo_valores_invalidos(client):
    r = client.post("/vehiculos/nuevo", data={**VEHICULO, "id_marca": "", "anio": "1950",
                                              "placa": "12-ABC", "kilometraje": "-1",
                                              "precio_venta": "0", "tipo": "Avión"})
    html = r.get_data(as_text=True)
    assert "«Marca» es obligatorio" in html
    assert "mayor o igual a 1980" in html
    assert "formato ABC123" in html
    assert "«Kilometraje» debe ser mayor o igual a 0" in html
    assert "mayor que 0" in html
    assert "«Tipo» no es una opción válida" in html


def test_vehiculo_placa_duplicada(client):
    r = client.post("/vehiculos/nuevo", data={**VEHICULO, "placa": "JKL482"})
    assert "Ya existe un registro" in r.get_data(as_text=True)


def test_vehiculo_con_marca_inexistente(client):
    r = client.post("/vehiculos/nuevo", data={**VEHICULO, "id_marca": "999999"})
    assert "relacionado" in r.get_data(as_text=True)


# ---------------------------------------------------------------- clientes

CLIENTE = {"documento": "999000111", "nombre_cliente": PREFIJO + "Cliente",
           "telefono": "3100000000", "email": "zz_test@ejemplo.co", "ciudad": "Neiva"}


def test_crud_clientes(client):
    r = client.post("/clientes/nuevo", data=CLIENTE, follow_redirects=True)
    assert "Cliente creado" in r.get_data(as_text=True)
    id_ = sql("SELECT id_cliente FROM clientes WHERE documento=%s", ("999000111",))[0]

    r = client.post(f"/clientes/{id_}/editar", data={**CLIENTE, "ciudad": "Pitalito", "email": ""},
                    follow_redirects=True)
    assert "actualizado" in r.get_data(as_text=True)
    assert sql("SELECT ciudad, email FROM clientes WHERE id_cliente=%s", (id_,)) == ("Pitalito", None)

    client.post(f"/clientes/{id_}/eliminar")
    assert sql("SELECT COUNT(*) FROM clientes WHERE id_cliente=%s", (id_,))[0] == 0


def test_cliente_documento_duplicado_y_datos_invalidos(client):
    r = client.post("/clientes/nuevo", data={**CLIENTE, "documento": "1075234567"})
    assert "Ya existe un registro" in r.get_data(as_text=True)
    r = client.post("/clientes/nuevo", data={**CLIENTE, "documento": "12ab", "telefono": "abc",
                                             "email": "malo"})
    html = r.get_data(as_text=True)
    assert "«Documento» debe tener solo números" in html
    assert "«Teléfono» debe tener solo números" in html
    assert "formato válido" in html


def test_no_elimina_cliente_con_operaciones(client):
    r = client.post("/clientes/1/eliminar", follow_redirects=True)
    assert "relacionado" in r.get_data(as_text=True)


# ---------------------------------------------------------------- asesores

ASESOR = {"nombre_asesor": PREFIJO + "Asesor", "telefono": "3200000000",
          "email": "zz_asesor@compraventa.co", "porcentaje_comision": "1.5"}


def test_crud_asesores(client):
    r = client.post("/asesores/nuevo", data=ASESOR, follow_redirects=True)
    assert "Asesor creado" in r.get_data(as_text=True)
    id_ = sql("SELECT id_asesor FROM asesores WHERE nombre_asesor=%s", (PREFIJO + "Asesor",))[0]

    r = client.post(f"/asesores/{id_}/editar", data={**ASESOR, "porcentaje_comision": "2.75"},
                    follow_redirects=True)
    assert "actualizado" in r.get_data(as_text=True)
    assert float(sql("SELECT porcentaje_comision FROM asesores WHERE id_asesor=%s", (id_,))[0]) == 2.75

    client.post(f"/asesores/{id_}/eliminar")
    assert sql("SELECT COUNT(*) FROM asesores WHERE id_asesor=%s", (id_,))[0] == 0


def test_asesor_comision_fuera_de_rango_y_email_duplicado(client):
    r = client.post("/asesores/nuevo", data={**ASESOR, "porcentaje_comision": "15"})
    assert "menor o igual a 10" in r.get_data(as_text=True)
    r = client.post("/asesores/nuevo", data={**ASESOR, "email": "carolina.munoz@compraventa.co"})
    assert "Ya existe un registro" in r.get_data(as_text=True)


def test_no_elimina_asesor_con_operaciones(client):
    r = client.post("/asesores/1/eliminar", follow_redirects=True)
    assert "relacionado" in r.get_data(as_text=True)


# ---------------------------------------------------------------- operaciones

OPERACION = {"fecha": "2026-11-05", "tipo_operacion": "Venta", "id_vehiculo": "1",
             "id_cliente": "2", "id_asesor": "3", "valor": "57000000", "forma_pago": "Crédito",
             "observaciones": PREFIJO + "prueba"}


def test_crud_operaciones(client):
    antes = contar("operaciones")
    r = client.post("/operaciones/nuevo", data=OPERACION, follow_redirects=True)
    assert "Operación registrada" in r.get_data(as_text=True)
    id_ = sql("SELECT id_operacion FROM operaciones WHERE observaciones=%s",
              (PREFIJO + "prueba",))[0]

    r = client.post(f"/operaciones/{id_}/editar",
                    data={**OPERACION, "tipo_operacion": "Compra", "valor": "50000000"},
                    follow_redirects=True)
    assert "actualizada" in r.get_data(as_text=True)
    tipo, valor = sql("SELECT tipo_operacion, valor FROM operaciones WHERE id_operacion=%s", (id_,))
    assert tipo == "Compra" and float(valor) == 50000000

    client.post(f"/operaciones/{id_}/eliminar")
    assert contar("operaciones") == antes


def test_operacion_invalida(client):
    r = client.post("/operaciones/nuevo", data={**OPERACION, "fecha": "", "tipo_operacion": "Regalo",
                                                "id_cliente": "", "valor": "-10"})
    html = r.get_data(as_text=True)
    assert "«Fecha» es obligatorio" in html
    assert "«Tipo de operación» no es una opción válida" in html
    assert "«Cliente» es obligatorio" in html
    assert "«Valor» debe ser mayor que 0" in html


def test_operacion_con_vehiculo_inexistente(client):
    r = client.post("/operaciones/nuevo", data={**OPERACION, "id_vehiculo": "999999"})
    assert "relacionado" in r.get_data(as_text=True)


def test_eliminar_inexistente(client):
    r = client.post("/operaciones/999999/eliminar", follow_redirects=True)
    assert "no existe" in r.get_data(as_text=True)


# ---------------------------------------------------------------- inicio de sesión

@pytest.mark.parametrize("ruta", ["/panel", "/marcas/", "/vehiculos/nuevo", "/operaciones/1/editar"])
def test_visitante_no_puede_entrar_a_la_administracion(anonimo, ruta):
    r = anonimo.get(ruta)
    assert r.status_code == 302 and "/login" in r.headers["Location"]


def test_visitante_no_puede_eliminar(anonimo):
    r = anonimo.post("/marcas/10/eliminar")
    assert r.status_code == 302 and "/login" in r.headers["Location"]
    assert sql("SELECT COUNT(*) FROM marcas WHERE id_marca=10")[0] == 1


def test_login_incorrecto(anonimo):
    r = anonimo.post("/login", data={"usuario": "admin", "clave": "mala"})
    assert "incorrectos" in r.get_data(as_text=True)
    assert anonimo.get("/panel").status_code == 302


def test_login_correcto_y_salir(anonimo):
    r = anonimo.post("/login?next=/clientes/", data={"usuario": "admin", "clave": CLAVE_PRUEBA})
    assert r.status_code == 302 and r.headers["Location"].endswith("/clientes/")
    assert anonimo.get("/panel").status_code == 200
    anonimo.post("/logout")
    assert anonimo.get("/panel").status_code == 302


def test_login_no_redirige_a_otro_sitio(anonimo):
    r = anonimo.post("/login?next=//sitio-malo.com", data={"usuario": "admin", "clave": CLAVE_PRUEBA})
    assert r.headers["Location"].endswith("/panel")


def test_catalogo_publico(anonimo):
    html = anonimo.get("/").get_data(as_text=True)
    assert "Onix LTZ" in html                  # disponible
    assert "Picanto Vibrant" in html           # reservado
    assert "Duster Intens" not in html         # vendido: no se muestra
    assert "/editar" not in html and "/eliminar" not in html
    assert "fotos/jkl482.jpg" in html


# ---------------------------------------------------------------- fotos

PNG_MINIMO = b"\x89PNG\r\n\x1a\n" + b"\x00" * 32


def test_subir_y_quitar_foto(client):
    datos = {**VEHICULO, "placa": "ZZF101", "linea": PREFIJO + "Foto",
             "foto": (io.BytesIO(PNG_MINIMO), "auto.png")}
    r = client.post("/vehiculos/nuevo", data=datos, content_type="multipart/form-data",
                    follow_redirects=True)
    assert "Vehículo creado" in r.get_data(as_text=True)
    id_, foto = sql("SELECT id_vehiculo, foto FROM vehiculos WHERE placa='ZZF101'")
    archivo = Path(client.application.static_folder) / "fotos" / foto
    try:
        assert foto.startswith("subidas/") and foto.endswith(".png") and archivo.exists()
        # editar sin subir otra foto la conserva; marcar "quitar" la elimina
        client.post(f"/vehiculos/{id_}/editar", data={**VEHICULO, "placa": "ZZF101"})
        assert sql("SELECT foto FROM vehiculos WHERE id_vehiculo=%s", (id_,))[0] == foto
        client.post(f"/vehiculos/{id_}/editar", data={**VEHICULO, "placa": "ZZF101", "quitar_foto": "1"})
        assert sql("SELECT foto FROM vehiculos WHERE id_vehiculo=%s", (id_,))[0] is None
    finally:
        archivo.unlink(missing_ok=True)
        client.post(f"/vehiculos/{id_}/eliminar")


def test_rechaza_archivo_que_no_es_imagen(client):
    datos = {**VEHICULO, "placa": "ZZF102",
             "foto": (io.BytesIO(b"esto no es una imagen"), "virus.png")}
    r = client.post("/vehiculos/nuevo", data=datos, content_type="multipart/form-data")
    assert "debe ser una imagen" in r.get_data(as_text=True)
    assert sql("SELECT COUNT(*) FROM vehiculos WHERE placa='ZZF102'")[0] == 0


# ---------------------------------------------------------------- integridad final

def test_datos_originales_intactos():
    for tabla in TABLAS:
        assert contar(tabla) == 10, tabla
