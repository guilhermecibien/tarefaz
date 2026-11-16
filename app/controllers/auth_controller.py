from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models import user

auth_bp = Blueprint("auth", __name__)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Faça login para acessar esta página.", "erro")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)
    return wrapped_view


@auth_bp.route("/")
def index():
    return redirect(url_for("tasks.index") if "user_id" in session else url_for("auth.login"))


@auth_bp.route("/cadastro", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        if not nome or not email or not senha:
            flash("Preencha nome, e-mail e senha.", "erro")
        elif "@" not in email:
            flash("Informe um e-mail válido.", "erro")
        elif user.validar_senha(senha):
            flash(user.validar_senha(senha), "erro")
        elif user.get_by_email(email):
            flash("Já existe uma conta com este e-mail.", "erro")
        else:
            user.create(nome, email, senha)
            flash("Cadastro realizado. Agora faça login.", "sucesso")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        senha = request.form.get("senha", "")
        account = user.get_by_email(email)
        if not user.password_is_valid(account, senha):
            flash("E-mail ou senha inválidos.", "erro")
        else:
            session.clear()
            session["user_id"] = account["id"]
            session["user_name"] = account["nome"]
            return redirect(url_for("tasks.index"))
    return render_template("auth/login.html")


@auth_bp.route("/logout", methods=("POST",))
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("auth.login"))


@auth_bp.route("/conta", methods=("GET", "POST"))
@login_required
def account():
    conta = user.get_by_id(session["user_id"])
    if request.method == "POST":
        senha_atual = request.form.get("senha_atual", "")
        if not user.password_is_valid(conta, senha_atual):
            flash("A senha atual está incorreta.", "erro")
        elif request.form.get("acao") == "senha":
            nova = request.form.get("nova_senha", "")
            if user.validar_senha(nova):
                flash(user.validar_senha(nova), "erro")
            elif nova != request.form.get("confirmar_senha", ""):
                flash("A confirmação não confere com a nova senha.", "erro")
            else:
                user.update_password(conta["id"], nova)
                flash("Senha alterada.", "sucesso")
                return redirect(url_for("auth.account"))
        else:
            nome = request.form.get("nome", "").strip()
            email = request.form.get("email", "").strip().lower()
            outro = user.get_by_email(email)
            if not nome or not email:
                flash("Preencha nome e e-mail.", "erro")
            elif "@" not in email:
                flash("Informe um e-mail válido.", "erro")
            elif outro and outro["id"] != conta["id"]:
                flash("Já existe uma conta com este e-mail.", "erro")
            else:
                user.update_profile(conta["id"], nome, email)
                session["user_name"] = nome
                flash("Dados atualizados.", "sucesso")
                return redirect(url_for("auth.account"))
    return render_template("auth/account.html", conta=conta)
