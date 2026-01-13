from enum import Enum


class PerfilAcesso(str, Enum):
    ADMIN = "ADMIN"
    USUARIO = "USUARIO"
