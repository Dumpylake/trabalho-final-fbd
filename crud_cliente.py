from fastapi import APIRouter, HTTPException
from db import get_connection
from models import cliente, clienteUpdate
from typing import List

router = APIRouter()

@router.post("/clientes")
async def criar_cliente(cli: cliente):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO cliente (id_cliente, nome, rua, numero, bairro, recepcionista_cpf) VALUES (%s, %s, %s, %s, %s, %s)",
            (cli.id_cliente, cli.nome, cli.rua, cli.numero, cli.bairro, cli.recepcionista_cpf)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao criar cliente: {e}")
    finally:
        cur.close()
        conn.close()
    return {"msg": "Cliente criado com sucesso"}

@router.get("/clientes", response_model=List[cliente])
async def listar_clientes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nome, rua, numero, bairro, recepcionista_cpf FROM cliente")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [cliente(id_cliente=r[0], nome=r[1], rua=r[2], numero=r[3], bairro=r[4], recepcionista_cpf=r[5]) for r in rows]

@router.get("/clientes/{id_cliente}", response_model=cliente)
async def get_cliente(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente, nome, rua, numero, bairro, recepcionista_cpf FROM cliente WHERE id_cliente=%s", (id_cliente,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return cliente(id_cliente=row[0], nome=row[1], rua=row[2], numero=row[3], bairro=row[4], recepcionista_cpf=row[5])
    raise HTTPException(404, "Cliente não encontrado")

@router.patch("/clientes/{id_cliente}")
async def atualizar_cliente(id_cliente: int, cli: clienteUpdate):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_cliente FROM cliente WHERE id_cliente=%s", (id_cliente,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(404, "Cliente não encontrado")

    campos = []
    valores = []
    for campo, valor in cli.dict(exclude_unset=True).items():
        campos.append(f"{campo}=%s")
        valores.append(valor)

    if not campos:
        cur.close()
        conn.close()
        raise HTTPException(400, "Nenhum campo informado para atualização")

    valores.append(id_cliente)

    try:
        cur.execute(f"UPDATE cliente SET {', '.join(campos)} WHERE id_cliente=%s", valores)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Erro ao atualizar cliente: {e}")
    finally:
        cur.close()
        conn.close()

    return {"msg": "Cliente atualizado com sucesso"}

@router.delete("/clientes/{id_cliente}")
async def deletar_cliente(id_cliente: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM cliente WHERE id_cliente=%s", (id_cliente,))
    conn.commit()
    cur.close()
    conn.close()
    return {"msg": "Cliente removido com sucesso"}
