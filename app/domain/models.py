from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum

class LivroEmprestimoLink(SQLModel, table=True):
    __tablename__ = "livro_emprestimo"
    
    livro_id: Optional[int] = Field(default=None, foreign_key="livro.id", primary_key=True)
    emprestimo_id: Optional[int] = Field(default=None, foreign_key="emprestimo.id", primary_key=True)
    quantidade: int = Field(default=1)

class StatusEmprestimo(str, Enum):
    ATIVO = "ativo"
    DEVOLVIDO = "devolvido"
    ATRASADO = "atrasado"

class AutorBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    nacionalidade: str = Field(max_length=50)
    data_nascimento: Optional[datetime] = None
    biografia: Optional[str] = None
    email: Optional[str] = None

class Autor(AutorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.now)
    
    # Relacionamento 1:N com Livro
    livros: List["Livro"] = Relationship(back_populates="autor")

class AutorCreate(AutorBase):
    pass

class AutorRead(AutorBase):
    id: int
    data_criacao: datetime

class AutorUpdate(SQLModel):
    nome: Optional[str] = None
    nacionalidade: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    biografia: Optional[str] = None
    email: Optional[str] = None

class EditoraBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    endereco: str = Field(max_length=200)
    telefone: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None

class Editora(EditoraBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.now)
    
    # Relacionamento 1:N com Livro
    livros: List["Livro"] = Relationship(back_populates="editora")

class EditoraCreate(EditoraBase):
    pass

class EditoraRead(EditoraBase):
    id: int
    data_criacao: datetime

class EditoraUpdate(SQLModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None

# Modelo Livro
class LivroBase(SQLModel):
    titulo: str = Field(min_length=1, max_length=200)
    isbn: str = Field(min_length=10, max_length=17, unique=True)
    ano_publicacao: int = Field(gt=1000, le=datetime.now().year)
    genero: str = Field(max_length=50)
    paginas: int = Field(gt=0)

class Livro(LivroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.now)
    
    # Relacionamentos
    autor_id: int = Field(foreign_key="autor.id")
    editora_id: int = Field(foreign_key="editora.id")
    
    autor: Autor = Relationship(back_populates="livros")
    editora: Editora = Relationship(back_populates="livros")
    
    # Relacionamento N:N com Empréstimo
    emprestimos: List["Emprestimo"] = Relationship(
        back_populates="livros", 
        link_model=LivroEmprestimoLink
    )

class LivroCreate(LivroBase):
    autor_id: int
    editora_id: int

class LivroRead(LivroBase):
    id: int
    data_criacao: datetime
    autor_id: int
    editora_id: int

class LivroUpdate(SQLModel):
    titulo: Optional[str] = None
    isbn: Optional[str] = None
    ano_publicacao: Optional[int] = None
    genero: Optional[str] = None
    paginas: Optional[int] = None
    autor_id: Optional[int] = None
    editora_id: Optional[int] = None

# Modelo Usuario
class UsuarioBase(SQLModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(max_length=100, unique=True)
    telefone: Optional[str] = None
    endereco: str = Field(max_length=200)
    cpf: str = Field(min_length=11, max_length=14, unique=True)

class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_criacao: datetime = Field(default_factory=datetime.now)
    ativo: bool = Field(default=True)
    
    # Relacionamento 1:N com Empréstimo
    emprestimos: List["Emprestimo"] = Relationship(back_populates="usuario")

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioRead(UsuarioBase):
    id: int
    data_criacao: datetime
    ativo: bool

class UsuarioUpdate(SQLModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None
    cpf: Optional[str] = None
    ativo: Optional[bool] = None

# Modelo Emprestimo
class EmprestimoBase(SQLModel):
    data_emprestimo: datetime = Field(default_factory=datetime.now)
    data_devolucao_prevista: datetime
    observacoes: Optional[str] = None

class Emprestimo(EmprestimoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data_devolucao_real: Optional[datetime] = None
    status: StatusEmprestimo = Field(default=StatusEmprestimo.ATIVO)
    
    # Relacionamentos
    usuario_id: int = Field(foreign_key="usuario.id")
    
    usuario: Usuario = Relationship(back_populates="emprestimos")
    
    # Relacionamento N:N com Livro
    livros: List[Livro] = Relationship(
        back_populates="emprestimos", 
        link_model=LivroEmprestimoLink
    )

class EmprestimoCreate(EmprestimoBase):
    usuario_id: int
    livro_ids: List[int] = Field(min_items=1)

class EmprestimoRead(EmprestimoBase):
    id: int
    data_devolucao_real: Optional[datetime] = None
    status: StatusEmprestimo
    usuario_id: int

class EmprestimoReadWithLivros(EmprestimoRead):
    livros: List[LivroRead] = []

class EmprestimoUpdate(SQLModel):
    data_devolucao_prevista: Optional[datetime] = None
    data_devolucao_real: Optional[datetime] = None
    status: Optional[StatusEmprestimo] = None
    observacoes: Optional[str] = None
