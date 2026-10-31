from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from datetime import datetime
from models import (
    init_db,
    buscar_usuario_por_email,
    buscar_usuario_por_id,
    verificar_senha,
    listar_aulas,
    adicionar_aula as db_adicionar_aula,
    remover_aula as db_remover_aula,
)

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.secret_key = "chave-temporaria-trocar-em-producao"

# Cria tabelas ao iniciar
init_db()


# ---------------------------------------------------------------------------
# Autenticação simples via session (sem Flask-Login)
# ---------------------------------------------------------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar a área de gestão.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.context_processor
def inject_user():
    """Disponibiliza 'usuario_logado' em todos os templates."""
    user = None
    if "user_id" in session:
        user = buscar_usuario_por_id(session["user_id"])
    return {"usuario_logado": user}


# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

DIAS = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
]

TURNOS = [
    {"key": "manha", "label": "Manhã", "horario": "7:30 – 12:00"},
    {"key": "tarde", "label": "Tarde", "horario": "13:00 – 17:30"},
    {"key": "noite", "label": "Noite", "horario": "18:30 – 22:00"},
]


# ---------------------------------------------------------------------------
# Rotas - Consulta (público)
# ---------------------------------------------------------------------------

def dia_da_semana_atual():
    """Retorna o dia da semana atual em português."""
    dias_py = {
        0: "Segunda-feira",
        1: "Terça-feira",
        2: "Quarta-feira",
        3: "Quinta-feira",
        4: "Sexta-feira",
        5: "Sábado",
        6: "Sábado",  # domingo mostra sábado
    }
    return dias_py[datetime.now().weekday()]


@app.route("/")
def consulta():
    dia = request.args.get("dia", dia_da_semana_atual())
    if dia not in DIAS:
        dia = "Segunda-feira"

    aulas_por_turno = {}
    for turno in TURNOS:
        aulas_por_turno[turno["key"]] = listar_aulas(dia, turno["key"])

    return render_template(
        "consulta.html",
        dias=DIAS,
        turnos=TURNOS,
        dia_atual=dia,
        aulas_por_turno=aulas_por_turno,
    )


# ---------------------------------------------------------------------------
# Rotas - Autenticação
# ---------------------------------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("admin"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = buscar_usuario_por_email(email)

        if usuario and verificar_senha(usuario, senha):
            session["user_id"] = usuario["id"]
            session["user_nome"] = usuario["nome"]
            return redirect(url_for("admin"))

        flash("E-mail ou senha incorretos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("consulta"))


# ---------------------------------------------------------------------------
# Rotas - Admin (protegidas)
# ---------------------------------------------------------------------------

@app.route("/admin")
@login_required
def admin():
    dia = request.args.get("dia", "Segunda-feira")
    if dia not in DIAS:
        dia = "Segunda-feira"

    aulas_por_turno = {}
    for turno in TURNOS:
        aulas_por_turno[turno["key"]] = listar_aulas(dia, turno["key"])

    return render_template(
        "admin.html",
        dias=DIAS,
        turnos=TURNOS,
        dia_atual=dia,
        aulas_por_turno=aulas_por_turno,
    )


@app.route("/admin/adicionar", methods=["POST"])
@login_required
def adicionar_aula():
    dia = request.form.get("dia_semana")
    turno = request.form.get("turno")
    turma = request.form.get("turma", "").strip()
    professor = request.form.get("professor", "").strip()
    curso = request.form.get("curso", "").strip()
    sala = request.form.get("sala", "").strip()

    if not all([dia, turno, turma, professor, curso, sala]):
        flash("Todos os campos são obrigatórios.", "error")
        return redirect(url_for("admin", dia=dia))

    if len(turma) != 4 or not turma.isdigit():
        flash("A turma deve ter exatamente 4 dígitos.", "error")
        return redirect(url_for("admin", dia=dia))

    db_adicionar_aula(dia, turno, turma, professor, curso, sala)
    flash(f"Aula da turma {turma} adicionada com sucesso!", "success")
    return redirect(url_for("admin", dia=dia))


@app.route("/admin/remover/<int:aula_id>", methods=["POST"])
@login_required
def remover_aula_route(aula_id):
    dia = db_remover_aula(aula_id)
    flash("Aula removida.", "success")
    return redirect(url_for("admin", dia=dia))


# ---------------------------------------------------------------------------
# Inicialização
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, port=5000)