from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine
from app.routers import router_usuario, router_livro, router_emprestimo
from app.exceptions import (
    value_error_handler,
    not_found_error_handler,
    validation_error_handler,
    generic_exception_handler,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Biblioteca Digital API",
    description="API para gerenciamento de usuários, livros e empréstimos",
    version="1.1.0"
)

# Routers
app.include_router(router_usuario.router)
app.include_router(router_livro.router)
app.include_router(router_emprestimo.router)

# Exception handlers
app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(LookupError, not_found_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)
