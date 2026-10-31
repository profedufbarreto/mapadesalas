from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Usuario(UserMixin, db.Model):
    """Usuários autorizados a cadastrar aulas (coordenação/secretaria)."""

    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)


class Aula(db.Model):
    """Cada registro representa uma turma alocada em uma sala/turno/dia."""

    __tablename__ = "aulas"

    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)      # Segunda-feira, Terça-feira...
    turno = db.Column(db.String(10), nullable=False)            # manha, tarde, noite
    turma = db.Column(db.String(4), nullable=False)             # código 4 dígitos
    professor = db.Column(db.String(120), nullable=False)
    curso = db.Column(db.String(200), nullable=False)
    sala = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "dia_semana": self.dia_semana,
            "turno": self.turno,
            "turma": self.turma,
            "professor": self.professor,
            "curso": self.curso,
            "sala": self.sala,
        }