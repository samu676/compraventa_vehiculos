"""Configuración de la aplicación. Los valores se leen del archivo .env"""
import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambia-esta-clave")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_NAME = os.getenv("DB_NAME", "compraventa_db")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")

    # Usuario administrador (el único que puede crear, editar y eliminar)
    ADMIN_USUARIO = os.getenv("ADMIN_USUARIO", "admin")
    ADMIN_CLAVE = os.getenv("ADMIN_CLAVE", "")

    # Tamaño máximo de las fotos que se suben (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
