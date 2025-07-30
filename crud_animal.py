from fastapi import APIRouter, HTTPException
from db import get_connection
from models import animal, animalUpdate
from typing import List

router = APIRouter()

@router.post("/animais")
async def criar_animal(a: animal):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO animal (num_registro, nome, alergias, peso, horario_atendimento, petshop_cnpj, veterinario_cpf) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (a.num_registro, a.nome, a.alergias, a.peso, a.horario_atendimento, a.petshop_cnpj, a.veterinario_cpf)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar animal: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Animal criado com sucesso"}

@router.get("/animais", response_model=List[animal])
async def listar_animais():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT num_registro, nome, alergias, peso, horario_atendimento, petshop_cnpj, veterinario_cpf FROM animal")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [animal(
        num_registro=r[0],
        nome=r[1],
        alergias=r[2],
        peso=r[3],
        horario_atendimento=r[4],
        petshop_cnpj=r[5],
        veterinario_cpf=r[6]
    ) for r in rows]

@router.get("/animais/{num_registro}", response_model=animal)
async def get_animal(num_registro: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT num_registro, nome, alergias, peso, horario_atendimento, petshop_cnpj, veterinario_cpf FROM animal WHERE num_registro=%s", (num_registro,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return animal(
            num_registro=row[0],
            nome=row[1],
            alergias=row[2],
            peso=row[3],
            horario_atendimento=row[4],
            petshop_cnpj=row[5],
            veterinario_cpf=row[6]
        )
    raise HTTPException(404, "Animal não encontrado")

@router.patch("/animais/{num_registro}")
async def atualizar_animal(num_registro: int, a: animalUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT num_registro FROM animal WHERE num_registro=%s", (num_registro,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Animal não encontrado")

    campos = []
    valores = []
    for campo, valor in a.dict(exclude_unset=True).items():
        campos.append(f"{campo}=%s")
        valores.append(valor)

    if not campos:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")

    valores.append(num_registro)

    try:
        cur.execute(f"UPDATE animal SET {', '.join(campos)} WHERE num_registro=%s", valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar animal: {e}")
    finally:
        cur.close()
        conn.close()

    return {"msg": "Animal atualizado com sucesso"}

@router.delete("/animais/{num_registro}")
async def deletar_animal(num_registro: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM animal WHERE num_registro=%s", (num_registro,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Animal removido com sucesso"}
