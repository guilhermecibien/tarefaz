from app.models.database import get_db


def listar(usuario_id, busca=None):
    sql = (
        "SELECT t.*,"
        " (SELECT COUNT(*) FROM itens WHERE tarefa_id = t.id) AS itens_total,"
        " (SELECT COUNT(*) FROM itens WHERE tarefa_id = t.id AND feito = 1) AS itens_feitos"
        " FROM tarefas t WHERE usuario_id = ?"
    )
    params = [usuario_id]
    if busca:
        sql += " AND (titulo LIKE ? OR descricao LIKE ?)"
        params += [f"%{busca}%"] * 2
    sql += " ORDER BY prioridade = 'alta' DESC, prazo IS NULL, prazo, id"
    return get_db().execute(sql, params).fetchall()


def get_by_id(task_id, usuario_id):
    return get_db().execute(
        "SELECT * FROM tarefas WHERE id = ? AND usuario_id = ?", (task_id, usuario_id)
    ).fetchone()


def create(titulo, descricao, importante, prazo, usuario_id):
    db = get_db()
    db.execute(
        "INSERT INTO tarefas (titulo, descricao, prioridade, prazo, usuario_id) VALUES (?, ?, ?, ?, ?)",
        (titulo.strip(), descricao.strip(), "alta" if importante else "media", prazo or None, usuario_id),
    )
    db.commit()


def update(task_id, titulo, descricao, importante, prazo, usuario_id):
    db = get_db()
    db.execute(
        "UPDATE tarefas SET titulo=?, descricao=?, prioridade=?, prazo=?, data_atualizacao=CURRENT_TIMESTAMP"
        " WHERE id=? AND usuario_id=?",
        (titulo.strip(), descricao.strip(), "alta" if importante else "media", prazo or None, task_id, usuario_id),
    )
    db.commit()


def renomear(task_id, titulo, usuario_id):
    db = get_db()
    db.execute(
        "UPDATE tarefas SET titulo=?, data_atualizacao=CURRENT_TIMESTAMP WHERE id=? AND usuario_id=?",
        (titulo.strip(), task_id, usuario_id),
    )
    db.commit()


def marcar(task_id, feita, usuario_id):
    db = get_db()
    db.execute(
        "UPDATE tarefas SET status=?, data_atualizacao=CURRENT_TIMESTAMP WHERE id=? AND usuario_id=?",
        ("concluido" if feita else "a_fazer", task_id, usuario_id),
    )
    db.commit()


def delete(task_id, usuario_id):
    db = get_db()
    db.execute("DELETE FROM tarefas WHERE id = ? AND usuario_id = ?", (task_id, usuario_id))
    db.commit()


def agrupar(tarefas, hoje):
    grupos = {"atrasadas": [], "hoje": [], "proximas": [], "sem_data": [], "feitas": []}
    for t in tarefas:
        if t["status"] == "concluido":
            grupos["feitas"].append(t)
        elif not t["prazo"]:
            grupos["sem_data"].append(t)
        elif t["prazo"] < hoje:
            grupos["atrasadas"].append(t)
        elif t["prazo"] == hoje:
            grupos["hoje"].append(t)
        else:
            grupos["proximas"].append(t)
    return grupos
