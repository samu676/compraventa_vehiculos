"""Validaciones de los formularios (se hacen en el servidor, antes de tocar la base)."""
import re
from datetime import date
from decimal import Decimal, InvalidOperation


def texto(form, campo, etiqueta, errores, obligatorio=True, max_len=None):
    valor = (form.get(campo) or "").strip()
    if obligatorio and not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
    if max_len and len(valor) > max_len:
        errores.append(f"«{etiqueta}» admite máximo {max_len} caracteres.")
    return valor or None


def entero(form, campo, etiqueta, errores, minimo=None, maximo=None):
    valor = (form.get(campo) or "").strip()
    if not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
        return None
    try:
        numero = int(valor)
    except ValueError:
        errores.append(f"«{etiqueta}» debe ser un número entero.")
        return None
    if minimo is not None and numero < minimo:
        errores.append(f"«{etiqueta}» debe ser mayor o igual a {minimo}.")
    if maximo is not None and numero > maximo:
        errores.append(f"«{etiqueta}» debe ser menor o igual a {maximo}.")
    return numero


def decimal(form, campo, etiqueta, errores, minimo=None, maximo=None, mayor_que=None):
    valor = (form.get(campo) or "").strip().replace(",", ".")
    if not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
        return None
    try:
        numero = Decimal(valor)
    except InvalidOperation:
        errores.append(f"«{etiqueta}» debe ser un número.")
        return None
    if not numero.is_finite():
        errores.append(f"«{etiqueta}» debe ser un número.")
        return None
    if mayor_que is not None and numero <= mayor_que:
        errores.append(f"«{etiqueta}» debe ser mayor que {mayor_que}.")
    if minimo is not None and numero < minimo:
        errores.append(f"«{etiqueta}» debe ser mayor o igual a {minimo}.")
    if maximo is not None and numero > maximo:
        errores.append(f"«{etiqueta}» debe ser menor o igual a {maximo}.")
    return numero


def fecha(form, campo, etiqueta, errores):
    valor = (form.get(campo) or "").strip()
    if not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        errores.append(f"«{etiqueta}» debe ser una fecha válida.")
        return None


def email(form, campo, etiqueta, errores, obligatorio=False):
    valor = (form.get(campo) or "").strip().lower()
    if obligatorio and not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
    elif valor and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", valor):
        errores.append(f"«{etiqueta}» no tiene un formato válido.")
    return valor or None


def opcion(form, campo, etiqueta, errores, opciones):
    """Valor que debe ser uno de los de la lista (para los <select> fijos)."""
    valor = (form.get(campo) or "").strip()
    if not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
        return None
    if valor not in opciones:
        errores.append(f"«{etiqueta}» no es una opción válida.")
    return valor


def patron(form, campo, etiqueta, errores, regex, mensaje, mayusculas=False):
    """Texto obligatorio que debe cumplir una expresión regular (placa, documento, teléfono)."""
    valor = (form.get(campo) or "").strip().replace(" ", "")
    if mayusculas:
        valor = valor.upper()
    if not valor:
        errores.append(f"El campo «{etiqueta}» es obligatorio.")
        return None
    if not re.fullmatch(regex, valor):
        errores.append(f"«{etiqueta}» {mensaje}")
    return valor
