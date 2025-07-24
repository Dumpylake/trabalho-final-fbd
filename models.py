from pydantic import BaseModel # type: ignore
from typing import List, Optional
from datetime import date

class animal(BaseModel):
    num_registro: int
    nome: str
    alergias: str
    peso: int
    horario_atendimento: int
    petshop_cnpj: int
    veterinario_cpf: int

class cachorro(BaseModel):
    animal_num_registro: int
    especie: str
    altura: int
    porte: str

class chinchila(BaseModel):
    animal_num_registro: int
    especie: str

class gato(BaseModel):
    animal_num_registro: int
    especie: str
    
class petshop(BaseModel):
    cnpj: int
    nome: str
    endereco: str

class petshopUpdate(BaseModel):
    nome: str
    endereco: str

class petshop_telefones(BaseModel):
    petshop_cnpj: int
    telefone: int
    
class cliente(BaseModel):
    id_cliente: int
    nome: str
    rua: str
    numero: int
    bairro: str
    recepcionista_cpf: int

class cliente_celulares(BaseModel):
    cliente_id: int
    celular: int
    
class empregados(BaseModel):
    cpf: int
    nome: str
    telefone: int
    data_contratacao: int
    petshop_cnpj: int

class veterinario(BaseModel):
    empregado_cpf: int
    crmv: int
    chefe_cpf: int

class veterinario_especializacoes(BaseModel):
    veterinario_cpf: int
    especializacao: str

class tratamento(BaseModel):
    animal_num_registro: int
    cliente_id: int
    motivo: str

class entregador(BaseModel):
    empregado_cpf: int
    cnh: int
    veiculo: str

class delivery(BaseModel):
    numero_do_pedido: int
    itens: str
    horario_do_pedido: int
    cliente_id: int
    entregador_cpf: int

class recepcionista(BaseModel):
    empregado_cpf: int
    telefone_do_petshop: int




