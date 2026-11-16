from app.models.database import get_db


def listar(tarefa_id):
    return get_db().execute(
        "SELECT * FROM itens WHERE tarefa_id = ? ORDER BY id", (tarefa_id,)
    ).fetchall()


def por_tarefa(usuario_id):
    """Todos os itens do usuário, agrupados pelo id da tarefa."""
    linhas = get_db().execute(
        "SELECT i.* FROM itens i JOIN tarefas t ON t.id = i.tarefa_id WHERE t.usuario_id = ? ORDER BY i.id",
        (usuario_id,),
    ).fetchall()
    grupos = {}
    for linha in linhas:
        grupos.setdefault(linha["tarefa_id"], []).append(linha)
    return grupos


def criar(tarefa_id, texto):
    db = get_db()
    db.execute("INSERT INTO itens (tarefa_id, texto) VALUES (?, ?)", (tarefa_id, texto.strip()))
    db.commit()


def marcar(item_id, tarefa_id, feito):
    db = get_db()
    db.execute("UPDATE itens SET feito = ? WHERE id = ? AND tarefa_id = ?", (1 if feito else 0, item_id, tarefa_id))
    db.commit()


def excluir(item_id, tarefa_id):
    db = get_db()
    db.execute("DELETE FROM itens WHERE id = ? AND tarefa_id = ?", (item_id, tarefa_id))
    db.commit()
