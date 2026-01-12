from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    perfil_acesso = Column(String(10), nullable=False)

    # Relacionamento com empréstimos (1 usuário -> N empréstimos)
    emprestimos = relationship(
        "Emprestimo",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )
