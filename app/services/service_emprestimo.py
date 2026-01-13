from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.models.model_emprestimo import Emprestimo
from app.repositories.repository_usuario import UsuarioRepository
from app.repositories.repository_livro import LivroRepository
from app.repositories.repository_emprestimo import EmprestimoRepository
from app.logger import get_logger

logger = get_logger(__name__)


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

        logger.info(
            "Tentativa de empréstimo | usuario=%s | livro=%s",
            id_usuario,
            id_livro
        )

        usuario = UsuarioRepository.get_by_id(db, id_usuario)
        if not usuario:
            logger.warning("Usuário não encontrado | id=%s", id_usuario)
            raise ValueError("Usuário não encontrado")

        livro = LivroRepository.get_by_id(db, id_livro)
        if not livro:
            logger.warning("Livro não encontrado | id=%s", id_livro)
            raise ValueError("Livro não encontrado")

        emprestimos_ativos = UsuarioRepository.count_emprestimos_ativos(
            db, id_usuario
        )
        if emprestimos_ativos >= 3:
            logger.warning(
                "Limite de empréstimos atingido | usuario=%s",
                id_usuario
            )
            raise ValueError("Usuário atingiu o limite de empréstimos")

        if livro.copias_disponiveis <= 0:
            logger.warning(
                "Livro sem cópias disponíveis | livro=%s",
                id_livro
            )
            raise ValueError("Não há cópias disponíveis deste livro")

        if EmprestimoRepository.existe_emprestimo_ativo_do_livro(
            db, id_usuario, id_livro
        ):
            logger.warning(
                "Usuário já está com este livro | usuario=%s | livro=%s",
                id_usuario,
                id_livro
            )
            raise ValueError("Usuário já está com este livro")

        hoje = data_emprestimo or date.today()
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

        logger.info(
            "Empréstimo realizado | emprestimo=%s | usuario=%s | livro=%s",
            emprestimo.id_emprestimo,
            id_usuario,
            id_livro
        )

        return emprestimo

    @staticmethod
    def devolver_livro(db: Session, id_emprestimo: int) -> Emprestimo:

        logger.info(
            "Tentativa de devolução | emprestimo=%s",
            id_emprestimo
        )

        emprestimo = EmprestimoRepository.get_by_id(db, id_emprestimo)
        if not emprestimo:
            logger.warning(
                "Empréstimo não encontrado | id=%s",
                id_emprestimo
            )
            raise ValueError("Empréstimo não encontrado")

        if emprestimo.status == "DEVOLVIDO":
            logger.warning(
                "Empréstimo já devolvido | id=%s",
                id_emprestimo
            )
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
        EmprestimoRepository.update(db, emprestimo)

        logger.info(
            "Livro devolvido | emprestimo=%s | multa=%.2f",
            id_emprestimo,
            multa
        )

        return emprestimo

    @staticmethod
    def listar_emprestimos_atuais(
        db: Session,
        page: int = 1,
        size: int = 10
    ):
        return EmprestimoRepository.list_atuais(db, page, size)

    @staticmethod
    def listar_historico_emprestimos(
        db: Session,
        page: int = 1,
        size: int = 10
    ):
        return EmprestimoRepository.list_historico(db, page, size)
    
    @staticmethod
    def listar_emprestimos_por_usuario(
        db: Session,
        id_usuario: int,
        page: int = 1,
        size: int = 10
    ):
        usuario = UsuarioRepository.get_by_id(db, id_usuario)
        if not usuario:
            raise ValueError("Usuário não encontrado")

        return EmprestimoRepository.list_by_usuario(
            db=db,
            id_usuario=id_usuario,
            page=page,
            size=size
        )
 
