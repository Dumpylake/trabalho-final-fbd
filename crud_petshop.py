from fastapi import APIRouter, HTTPException # type: ignore
from db import get_connection
from models import petshop
from typing import List, Optional
from models import petshopUpdate

router = APIRouter()

@router.post("/petshop")
async def criar_petshop(pet: petshop):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO petshop (cnpj, nome, endereço) VALUES (%s, %s, %s)",
            (pet.cnpj, pet.nome, pet.endereco)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar petshop: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "petshop criado com sucesso"}

@router.get("/petshop", response_model=List[petshop])
async def listar_departamentos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cnpj, nome, endereco FROM petshop")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        petshop(
            cnpj=d[0], nome=d[1], endereco=d[2]
        ) for d in rows
    ]

@router.get("/petshop/{cnpj}", response_model=petshop)
async def get_petshop(cnpj : int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cnpj, nome, endereco FROM petshop WHERE dnumero=%s", (cnpj,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return petshop(cnpj=row[0], nome=row[1], endereco=row[2])
    raise HTTPException(404, "Petshop não encontrado")


@router.patch("/petshop/{cnpj}")
async def atualizar_petshop_parcial(cnpj: int, pet: petshopUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT cnpj FROM petshop WHERE cnpj=%s", (cnpj,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Petshop não encontrado")
    fields = []
    values = []
    for campo, valor in pet.dict(exclude_unset=True).items():
        fields.append(f"{campo}=%s")
        values.append(valor)
    if not fields:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")
    values.append(cnpj)
    try:
        cur.execute(f"UPDATE petshop SET {', '.join(fields)} WHERE cnpj=%s", values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "petshop atualizado"}

@router.delete("/petshop/{cnpj}")
async def deletar_petshop(cnpj: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM petshop WHERE cnpj=%s", (cnpj,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "petshop removido"}