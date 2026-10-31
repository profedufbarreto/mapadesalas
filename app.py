from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from config import Config
from models import db, Usuario, Aula

# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.login_message = "Faça login para acessar a área de gestão."
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


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


@app.route("/")
def consulta():
    """Página pública — alunos consultam o mapa de salas."""
    dia = request.args.get("dia", "Segunda-feira")
    if dia not in DIAS:
        dia = "Segunda-feira"

    aulas_por_turno = {}
    for turno in TURNOS:
        aulas_por_turno[turno["key"]] = (
            Aula.query.filter_by(dia_semana=dia, turno=turno["key"])
            .order_by(Aula.sala, Aula.turma)
            .all()
        )

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
    if current_user.is_authenticated:
        return redirect(url_for("admin"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            proximo = request.args.get("next")
            return redirect(proximo or url_for("admin"))

        flash("E-mail ou senha incorretos.", "error")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("consulta"))


# ---------------------------------------------------------------------------
# Rotas - Admin (protegidas)
# ---------------------------------------------------------------------------


@app.route("/admin")
@login_required
def admin():
    """Painel de gestão — cadastrar/remover aulas."""
    dia = request.args.get("dia", "Segunda-feira")
    if dia not in DIAS:
        dia = "Segunda-feira"

    aulas_por_turno = {}
    for turno in TURNOS:
        aulas_por_turno[turno["key"]] = (
            Aula.query.filter_by(dia_semana=dia, turno=turno["key"])
            .order_by(Aula.sala, Aula.turma)
            .all()
        )

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

    # Validação simples
    if not all([dia, turno, turma, professor, curso, sala]):
        flash("Todos os campos são obrigatórios.", "error")
        return redirect(url_for("admin", dia=dia))

    if len(turma) != 4 or not turma.isdigit():
        flash("A turma deve ter exatamente 4 dígitos.", "error")
        return redirect(url_for("admin", dia=dia))

    aula = Aula(
        dia_semana=dia,
        turno=turno,
        turma=turma,
        professor=professor,
        curso=curso,
        sala=sala,
    )
    db.session.add(aula)
    db.session.commit()

    flash(f"Aula da turma {turma} adicionada com sucesso!", "success")
    return redirect(url_for("admin", dia=dia))


@app.route("/admin/remover/<int:aula_id>", methods=["POST"])
@login_required
def remover_aula(aula_id):
    aula = Aula.query.get_or_404(aula_id)
    dia = aula.dia_semana
    db.session.delete(aula)
    db.session.commit()
    flash("Aula removida.", "success")
    return redirect(url_for("admin", dia=dia))


# ---------------------------------------------------------------------------
# Inicialização
# ---------------------------------------------------------------------------

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)