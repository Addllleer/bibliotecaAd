from datetime import date, timedelta
from sqlalchemy.orm import Session
from app.models.model_emprestimo import Emprestimo
from app.repositories.repository_usuario import UsuarioRepository
from app.repositories.repository_livro import LivroRepository
from app.repositories.repository_emprestimo import EmprestimoRepository


class EmprestimoService:

    PRAZO_PADRAO_DIAS = 14
    MULTA_POR_DIA = 2.0

    @staticmethod
    def realizar_emprestimo(
                        db: Session,
                        id_usuario: int,
                        id_livro: int,
                        data_emprestimo: date | None = None
                    ) -> Emprestimo:
        usuario = UsuarioRepository.get_by_id(db, id_usuario)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        livro = LivroRepository.get_by_id(db, id_livro)
        if not livro:
            raise ValueError("Livro não encontrado")

        emprestimos_ativos = UsuarioRepository.count_emprestimos_ativos(db, id_usuario)
        if emprestimos_ativos >= 3:
            raise ValueError("Usuário atingiu o limite de empréstimos")

        if livro.copias_disponiveis <= 0:
            raise ValueError("Não há cópias disponíveis deste livro")

        hoje = data_emprestimo if data_emprestimo else date.today()
        prazo_devolucao = hoje + timedelta(days=EmprestimoService.PRAZO_PADRAO_DIAS)

        emprestimo = Emprestimo(
            id_usuario=id_usuario,
            id_livro=id_livro,
            data_emprestimo=hoje,
            prazo_devolucao=prazo_devolucao,
            status="ATIVO"
        )

        livro.copias_disponiveis -= 1

        EmprestimoRepository.create(db, emprestimo)
        LivroRepository.update(db, livro)

        return emprestimo

    @staticmethod
    def devolver_livro(db: Session, id_emprestimo: int) -> Emprestimo:
        emprestimo = EmprestimoRepository.get_by_id(db, id_emprestimo)
        if not emprestimo:
            raise ValueError("Empréstimo não encontrado")

        if emprestimo.status == "DEVOLVIDO":
            raise ValueError("Empréstimo já devolvido")

        hoje = date.today()
        emprestimo.data_devolucao = hoje

        multa = 0.0
        if hoje > emprestimo.prazo_devolucao:
            dias_atraso = (hoje - emprestimo.prazo_devolucao).days
            multa = dias_atraso * EmprestimoService.MULTA_POR_DIA
            emprestimo.status = "ATRASADO"
        else:
            emprestimo.status = "DEVOLVIDO"

        emprestimo.multa = multa

        livro = LivroRepository.get_by_id(db, emprestimo.id_livro)
        livro.copias_disponiveis += 1

        LivroRepository.update(db, livro)
        EmprestimoRepository.create(db, emprestimo)

        return emprestimo

    @staticmethod
    def listar_emprestimos_atuais(db):
        return (
            db.query(Emprestimo)
            .filter(Emprestimo.status.in_(["ATIVO", "ATRASADO"]))
            .all()
        )
    
    @staticmethod
    def listar_historico_emprestimos(db):
        return db.query(Emprestimo).all()


