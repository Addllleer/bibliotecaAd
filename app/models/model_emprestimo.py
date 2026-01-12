from sqlalchemy import Column, Integer, Date, ForeignKey, Float, String
from sqlalchemy.orm import relationship

from app.database import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id_emprestimo = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("usuarios.id_usuario"), nullable=False)
    id_livro = Column(Integer, ForeignKey("livros.id_livro"), nullable=False)
    data_emprestimo = Column(Date, nullable=False)
    prazo_devolucao = Column(Date, nullable=False)
    data_devolucao = Column(Date, nullable=True)
    multa = Column(Float, nullable=True)
    status = Column(String(10), nullable=False)

    usuario = relationship(
        "Usuario",
        back_populates="emprestimos"
    )

    livro = relationship(
        "Livro",
        back_populates="emprestimos"
    )
