from datetime import date, datetime

from flask import Blueprint, abort, flash, jsonify, redirect, render_template, request, session, url_for

from app.controllers.auth_controller import login_required
from app.models import item, task

task_bp = Blueprint("tasks", __name__, url_prefix="/tarefas")


def validar(form):
    if not form.get("titulo", "").strip():
        return "Escreva o título da tarefa."
    prazo = form.get("prazo", "")
    if prazo:
        try:
            datetime.strptime(prazo, "%Y-%m-%d")
        except ValueError:
            return "A data informada não é válida."
    return None


@task_bp.route("/")
@login_required
def index():
    busca = request.args.get("q", "").strip()
    hoje = date.today().isoformat()
    tarefas = task.listar(session["user_id"], busca)
    grupos = task.agrupar(tarefas, hoje)
    pendentes = len(tarefas) - len(grupos["feitas"])
    return render_template(
        "tasks/index.html",
        grupos=grupos,
        pendentes=pendentes,
        busca=busca,
        hoje=hoje,
        itens=item.por_tarefa(session["user_id"]),
    )


@task_bp.route("/nova", methods=("POST",))
@login_required
def create():
    erro = validar(request.form)
    if erro:
        flash(erro, "erro")
    else:
        task.create(
            request.form["titulo"], "", False, request.form.get("prazo", ""), session["user_id"]
        )
    return redirect(url_for("tasks.index"))


@task_bp.route("/<int:task_id>/editar", methods=("GET", "POST"))
@login_required
def edit(task_id):
    tarefa = task.get_by_id(task_id, session["user_id"])
    if tarefa is None:
        abort(404)
    if request.method == "POST":
        erro = validar(request.form)
        if erro:
            flash(erro, "erro")
        else:
            task.update(
                task_id,
                request.form["titulo"],
                request.form.get("descricao", ""),
                "importante" in request.form,
                request.form.get("prazo", ""),
                session["user_id"],
            )
            return redirect(url_for("tasks.index"))
    return render_template("tasks/form.html", task=tarefa, itens=item.listar(task_id))


@task_bp.route("/<int:task_id>/titulo", methods=("POST",))
@login_required
def rename(task_id):
    if task.get_by_id(task_id, session["user_id"]) is None:
        abort(404)
    titulo = request.form.get("titulo", "").strip()
    if not titulo:
        return jsonify(erro="Escreva o título da tarefa."), 400
    task.renomear(task_id, titulo, session["user_id"])
    return jsonify(titulo=titulo)


@task_bp.route("/<int:task_id>/status", methods=("POST",))
@login_required
def toggle(task_id):
    if task.get_by_id(task_id, session["user_id"]) is None:
        abort(404)
    task.marcar(task_id, request.form.get("feita") == "1", session["user_id"])
    return redirect(url_for("tasks.index"))


@task_bp.route("/<int:task_id>/excluir", methods=("POST",))
@login_required
def delete(task_id):
    if task.get_by_id(task_id, session["user_id"]) is None:
        abort(404)
    task.delete(task_id, session["user_id"])
    flash("Tarefa excluída.", "sucesso")
    return redirect(url_for("tasks.index"))


def voltar_do_item(task_id):
    # os itens podem ser mexidos pela lista ou pela página de edição
    if request.form.get("next") == "lista":
        return redirect(url_for("tasks.index"))
    return redirect(url_for("tasks.edit", task_id=task_id) + "#checklist")


def tarefa_do_usuario(task_id):
    if task.get_by_id(task_id, session["user_id"]) is None:
        abort(404)


@task_bp.route("/<int:task_id>/itens", methods=("POST",))
@login_required
def add_item(task_id):
    tarefa_do_usuario(task_id)
    texto = request.form.get("texto", "").strip()
    if texto:
        item.criar(task_id, texto)
    return voltar_do_item(task_id)


@task_bp.route("/<int:task_id>/itens/<int:item_id>/feito", methods=("POST",))
@login_required
def check_item(task_id, item_id):
    tarefa_do_usuario(task_id)
    item.marcar(item_id, task_id, request.form.get("feito") == "1")
    return voltar_do_item(task_id)


@task_bp.route("/<int:task_id>/itens/<int:item_id>/excluir", methods=("POST",))
@login_required
def delete_item(task_id, item_id):
    tarefa_do_usuario(task_id)
    item.excluir(item_id, task_id)
    return voltar_do_item(task_id)
