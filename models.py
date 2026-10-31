"""
Camada de acesso ao banco de dados usando sqlite3 puro.
Sem dependência de SQLAlchemy — evita problemas com Device Guard.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "database.db")


def get_db():
    """Retorna uma conexão com o banco."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn


def init_db():
    """Cria as tabelas se não existirem."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dia_semana TEXT NOT NULL,
            turno TEXT NOT NULL,
            turma TEXT NOT NULL,
            professor TEXT NOT NULL,
            curso TEXT NOT NULL,
            sala TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


# ---------------------------------------------------------------------------
# Funções de Usuário
# ---------------------------------------------------------------------------

def criar_usuario(nome, email, senha):
    conn = get_db()
    senha_hash = generate_password_hash(senha)
    conn.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
        (nome, email, senha_hash),
    )
    conn.commit()
    conn.close()


def buscar_usuario_por_email(email):
    conn = get_db()
    user = conn.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    conn.close()
    return user


def buscar_usuario_por_id(user_id):
    conn = get_db()
    user = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    return user


def verificar_senha(usuario_row, senha):
    return check_password_hash(usuario_row["senha_hash"], senha)


# ---------------------------------------------------------------------------
# Funções de Aula
# ---------------------------------------------------------------------------

def listar_aulas(dia_semana, turno):
    conn = get_db()
    aulas = conn.execute(
        "SELECT * FROM aulas WHERE dia_semana = ? AND turno = ? ORDER BY sala, turma",
        (dia_semana, turno),
    ).fetchall()
    conn.close()
    return aulas


def adicionar_aula(dia_semana, turno, turma, professor, curso, sala):
    conn = get_db()
    conn.execute(
        "INSERT INTO aulas (dia_semana, turno, turma, professor, curso, sala) VALUES (?, ?, ?, ?, ?, ?)",
        (dia_semana, turno, turma, professor, curso, sala),
    )
    conn.commit()
    conn.close()


def remover_aula(aula_id):
    conn = get_db()
    aula = conn.execute("SELECT dia_semana FROM aulas WHERE id = ?", (aula_id,)).fetchone()
    dia = aula["dia_semana"] if aula else "Segunda-feira"
    conn.execute("DELETE FROM aulas WHERE id = ?", (aula_id,))
    conn.commit()
    conn.close()
    return dia