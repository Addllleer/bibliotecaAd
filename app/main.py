from fastapi import FastAPI
from app.database import Base, engine
from app.routers import router_usuario, router_livro, router_emprestimo

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Biblioteca Digital API",
    description="API para gerenciamento de usuários, livros e empréstimos",
    version="1.1.0"
)

app.include_router(router_usuario.router)
app.include_router(router_livro.router)
app.include_router(router_emprestimo.router)

