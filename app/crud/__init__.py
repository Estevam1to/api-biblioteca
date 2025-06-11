from app.crud.autores_crud import crud_autor
from app.crud.editoras_crud import crud_editora
from app.crud.emprestimos_crud import crud_emprestimo
from app.crud.livros_crud import crud_livro
from app.crud.usuarios_crud import crud_usuario

__all__ = [
    "crud_autor",
    "crud_editora", 
    "crud_livro",
    "crud_usuario",
    "crud_emprestimo",
]
