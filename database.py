import sqlite3
from datetime import datetime, timedelta

DB_FILE = "banco.db"

def db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    with db() as conn:
        c = conn.cursor()
        # Tabelas de usuários e VIP
        c.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                user_id TEXT PRIMARY KEY,
                nome TEXT,
                inicio TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS vips (
                user_id TEXT PRIMARY KEY,
                plano TEXT,
                inicio TEXT,
                fim TEXT
            )
        """)
        # Tabela de pagamentos
        c.execute("""
            CREATE TABLE IF NOT EXISTS pagamentos (
                txid TEXT PRIMARY KEY,
                user_id TEXT,
                plano TEXT,
                valor REAL,
                status TEXT
            )
        """)
        conn.commit()

def salvar_pagamento(txid, user_id, plano, valor):
    with db() as conn:
        c = conn.cursor()
        c.execute("INSERT INTO pagamentos VALUES (?, ?, ?, ?, ?)", (txid, user_id, plano, valor, "PENDENTE"))
        conn.commit()

def confirmar_pagamento(txid):
    with db() as conn:
        c = conn.cursor()
        c.execute("UPDATE pagamentos SET status='PAGO' WHERE txid=?", (txid,))
        conn.commit()
        c.execute("SELECT user_id, plano FROM pagamentos WHERE txid=?", (txid,))
        return c.fetchone()

def liberar_vip(user_id, plano, dias):
    inicio = datetime.now()
    fim = inicio + timedelta(days=dias)
    with db() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO vips (user_id, plano, inicio, fim)
            VALUES (?, ?, ?, ?)
        """, (user_id, plano, inicio.isoformat(), fim.isoformat()))
        conn.commit()
