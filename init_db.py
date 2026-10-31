"""
Script para inicializar o banco de dados e criar o primeiro usuario admin.

Uso:
    py -3.12 init_db.py

Cria o banco (database.db) e cadastra um usuario administrador.
Rode apenas uma vez, ou quando quiser resetar o banco.
"""

from models import get_db, init_db, criar_usuario

DADOS_EXEMPLO = [
    ("Segunda-feira", "manha", "2401", "Ana Souza", "Tecnico em Informatica", "Lab 01"),
    ("Segunda-feira", "manha", "2415", "Carlos Lima", "Programacao Web", "Lab 03"),
    ("Segunda-feira", "tarde", "2408", "Mariana Costa", "Design Grafico", "Sala 12"),
    ("Segunda-feira", "noite", "2422", "Eduardo Barreto", "Logica de Programacao", "Lab 02"),
    ("Segunda-feira", "noite", "2430", "Fernanda Reis", "Banco de Dados", "Lab 04"),
    ("Terca-feira", "manha", "2403", "Roberto Silva", "Redes de Computadores", "Lab 05"),
    ("Quarta-feira", "noite", "2422", "Eduardo Barreto", "Logica de Programacao", "Lab 02"),
]


def main():
    # Remove banco antigo e recria
    import os
    from models import DB_PATH
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    init_db()

    # Cria usuario admin
    criar_usuario("Administrador", "admin@senac.com", "20474720")

    # Insere dados de exemplo
    conn = get_db()
    for dia, turno, turma, prof, curso, sala in DADOS_EXEMPLO:
        conn.execute(
            "INSERT INTO aulas (dia_semana, turno, turma, professor, curso, sala) VALUES (?, ?, ?, ?, ?, ?)",
            (dia, turno, turma, prof, curso, sala),
        )
    conn.commit()
    conn.close()

    print("=" * 50)
    print("  Banco de dados criado com sucesso!")
    print("=" * 50)
    print()
    print("  Usuario admin criado:")
    print("    E-mail: admin@senac")
    print("    Senha:  20474720")
    print()
    print("  Dados de exemplo inseridos (7 aulas).")
    print()
    print("  Para rodar o servidor:")
    print("    py -3.12 app.py")
    print()
    print("  Acesse: http://localhost:5000")
    print("=" * 50)


if __name__ == "__main__":
    main()