from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Livro(Base):
    __tablename__ = "livros"

    id_livro = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    autor = Column(String(100), nullable=False)
    categoria = Column(String(20), nullable=False)
    localizacao = Column(String(2), nullable=False) 
    qtd_copias = Column(Integer, nullable=False)
    copias_disponiveis = Column(Integer, nullable=False)

    emprestimos = relationship(
        "Emprestimo",
        back_populates="livro",
        cascade="all, delete-orphan"
    )
