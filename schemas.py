from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MembrosBase(BaseModel):
    id_membro: int
    nome: str = Field(
        title="Nome do membro",
        max_length=25,
        example="Joao"
    )
    sobrenome: Optional[str] = Field(
        title="Sobrenome do membro",
        max_length=25,
        example="Macedo"
    )
    celular: Optional[int] = Field(
        title="Celular do membro com DDD de estado",
        example=11912345678
    )

    class Config:
        orm_mode = True

class MembrosCreate(MembrosBase):
    pass

class PlanosBase(BaseModel):
    id_plano: int
    nome: str = Field(
        title="Nome do plano",
        max_length=25,
        example="Plano 1 ano"
    )
    preco: float = Field(
        title="Preco do plano por mês, em reais",
        example=50.99
    )

    class Config:
        orm_mode = True

class PlanosCreate(PlanosBase):
    pass

class AssinaturasBase(BaseModel):
    id_assinatura: int
    ativo: bool = Field(
        title="Descreve se o membro tem o plano ativado ou não",
        example=True
    )
    data_ativacao: datetime = Field(
        title="Data de ativação do plano",
        example="2023-11-07T10:00:00"
    )

class AssinaturasCreate(AssinaturasBase):
    pass

class Assinaturas(AssinaturasBase):
    id_membro: int = Field(
        title="Número correspondente ao membro da academia",
        example=1
    )
    id_plano: int = Field(
        title="Número correspondente ao plano da academia",
        example=1
    )

    class Config:
        orm_mode = True
