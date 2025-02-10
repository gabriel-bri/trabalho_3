from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class Curso(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome_curso: str
    descricao: str
    # Referência para a categoria (ID do documento Categoria)
    categoria_id: Optional[str] = None  
    horas_totais: str
    # Lista de IDs dos módulos deste curso
    modulos: List[str] = []
    # Referência para o instrutor (ID do documento Instrutor)
    instrutor_id: str  
    # Lista de IDs de inscrições (para relacionar alunos)
    alunos: List[str] = []  


class Aluno(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome_completo: str
    descricao: Optional[str] = None
    contato_email: str
    # Lista de IDs de inscrições (N:N com Curso)
    cursos: List[str] = []
    # Lista de IDs dos certificados emitidos para o aluno
    certificados: List[str] = []


class Aula(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    titulo: str
    descricao: Optional[str] = None
    duracao: str
    material: Optional[str] = None
    # Referência para o módulo (ID do documento Modulo)
    modulo_id: Optional[str] = None


class Avaliacao(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    # IDs para os documentos relacionados
    curso_id: Optional[str] = None
    aluno_id: Optional[str] = None
    nota: float
    comentario: Optional[str] = None
    data_avaliacao: datetime = Field(default_factory=datetime.utcnow)


class Categoria(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome_categoria: str
    descricao: Optional[str] = None
    data_criacao: datetime = Field(default_factory=datetime.utcnow)
    # Se desejar, pode armazenar uma lista de IDs de cursos vinculados a essa categoria.
    cursos: List[str] = []


class Certificado(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    # Referências para os documentos de aluno e curso
    aluno_id: Optional[str] = None
    curso_id: Optional[str] = None
    data_emissao: datetime = Field(default_factory=datetime.utcnow)
    codigo_verificacao: str


class Inscricao(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    # Referências para aluno e curso
    aluno_id: Optional[str] = None
    curso_id: Optional[str] = None
    data_inscricao: datetime = Field(default_factory=datetime.utcnow)
    status: str  # Exemplo: "Ativo", "Concluído", "Cancelado"
    progresso: float = 0.0  # Percentual de conclusão (0.0 a 100.0)


class Instrutor(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome_completo: str
    descricao: Optional[str] = None
    especialidade: Optional[str] = None
    contato_email: str
    # Lista de IDs dos cursos ministrados
    cursos: List[str] = []


class Modulo(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    nome_modulo: str
    descricao: Optional[str] = None
    # Referência para o curso ao qual o módulo pertence
    curso_id: Optional[str] = None
    # Lista de IDs das aulas contidas no módulo
    aulas: List[str] = []


class Suporte(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    # Referências para aluno e curso
    aluno_id: Optional[str] = None
    curso_id: Optional[str] = None
    data_abertura: datetime = Field(default_factory=datetime.utcnow)
    descricao_problema: str
    status: str  # Exemplo: "Aberto", "Em Andamento", "Resolvido"