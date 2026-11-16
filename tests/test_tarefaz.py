from app.models import task

from conftest import login, register


def nova(client, titulo, prazo=""):
    return client.post("/tarefas/nova", data={"titulo": titulo, "prazo": prazo}, follow_redirects=True)


def test_cadastro_de_usuario(client):
    response = register(client)
    assert b"Cadastro realizado" in response.data


def test_login(client):
    register(client)
    response = login(client)
    assert "Olá, Maria" in response.get_data(as_text=True)


def test_criacao_de_tarefa(client):
    register(client)
    login(client)
    response = nova(client, "Estudar Flask", "2030-05-10")
    assert b"Estudar Flask" in response.data
    assert b"10/05/2030" in response.data


def test_tarefa_sem_titulo_e_rejeitada(client, app):
    register(client)
    login(client)
    response = nova(client, "   ")
    assert "Escreva o título" in response.get_data(as_text=True)
    with app.app_context():
        assert task.listar(1) == []


def test_concluir_e_reabrir(client, app):
    register(client)
    login(client)
    nova(client, "Atividade")
    client.post("/tarefas/1/status", data={"feita": "1"})
    with app.app_context():
        assert task.get_by_id(1, 1)["status"] == "concluido"
    client.post("/tarefas/1/status", data={"feita": "0"})
    with app.app_context():
        assert task.get_by_id(1, 1)["status"] == "a_fazer"


def test_atrasadas_aparecem_em_grupo_proprio(client):
    register(client)
    login(client)
    response = nova(client, "Boleto", "2020-01-01")
    assert b"Atrasadas" in response.data


def test_busca(client):
    register(client)
    login(client)
    nova(client, "Comprar pão")
    nova(client, "Ligar para o dentista")
    response = client.get("/tarefas/?q=dentista")
    assert b"dentista" in response.data
    assert "pão".encode() not in response.data


def test_editar_e_marcar_importante(client, app):
    register(client)
    login(client)
    nova(client, "Rascunho")
    client.post("/tarefas/1/editar", data={"titulo": "Final", "descricao": "", "prazo": "", "importante": "on"})
    with app.app_context():
        item = task.get_by_id(1, 1)
    assert item["titulo"] == "Final"
    assert item["prioridade"] == "alta"


def test_excluir(client, app):
    register(client)
    login(client)
    nova(client, "Apagar")
    client.post("/tarefas/1/excluir")
    with app.app_context():
        assert task.listar(1) == []


def test_usuario_visualiza_somente_proprias_tarefas(client, app):
    register(client, "Ana", "ana@email.com")
    login(client, "ana@email.com")
    nova(client, "Tarefa da Ana")
    client.post("/logout")
    register(client, "Bruno", "bruno@email.com")
    login(client, "bruno@email.com")
    nova(client, "Tarefa do Bruno")
    response = client.get("/tarefas/")
    assert b"Tarefa do Bruno" in response.data
    assert b"Tarefa da Ana" not in response.data
    assert client.get("/tarefas/1/editar").status_code == 404
    assert client.post("/tarefas/1/status", data={"feita": "1"}).status_code == 404
    assert client.post("/tarefas/1/excluir").status_code == 404


def test_renomear_pelo_titulo(client, app):
    register(client)
    login(client)
    nova(client, "Antigo")
    response = client.post("/tarefas/1/titulo", data={"titulo": "  Novo  "})
    assert response.get_json() == {"titulo": "Novo"}
    assert client.post("/tarefas/1/titulo", data={"titulo": " "}).status_code == 400
    with app.app_context():
        assert task.get_by_id(1, 1)["titulo"] == "Novo"


def test_rotulos_de_prazo():
    from datetime import date
    from app.datas import rotulo_prazo
    hoje = date(2026, 11, 16)  # segunda-feira
    assert rotulo_prazo("2026-11-16", hoje) == "Hoje"
    assert rotulo_prazo("2026-11-17", hoje) == "Amanhã"
    assert rotulo_prazo("2026-11-20", hoje) == "Sex"
    assert rotulo_prazo("2026-11-25", hoje) == "25/11"
    assert rotulo_prazo("2027-01-05", hoje) == "05/01/2027"
    assert rotulo_prazo("2026-11-15", hoje) == "Ontem"
    assert rotulo_prazo("2026-11-13", hoje) == "há 3 dias"
    assert rotulo_prazo("2026-08-01", hoje) == "01/08"
    assert rotulo_prazo(None, hoje) == ""


def test_trocar_email_e_nome(client):
    register(client)
    login(client)
    errada = client.post("/conta", data={"acao": "dados", "nome": "Maria S", "email": "nova@email.com", "senha_atual": "x"}, follow_redirects=True)
    assert "senha atual está incorreta" in errada.get_data(as_text=True)
    ok = client.post("/conta", data={"acao": "dados", "nome": "Maria S", "email": "nova@email.com", "senha_atual": "senha123"}, follow_redirects=True)
    assert b"Dados atualizados" in ok.data
    client.post("/logout")
    assert "Olá, Maria S" in login(client, "nova@email.com").get_data(as_text=True)


def test_email_ja_usado_e_rejeitado(client):
    register(client, "Ana", "ana@email.com")
    register(client)
    login(client)
    response = client.post("/conta", data={"acao": "dados", "nome": "Maria", "email": "ana@email.com", "senha_atual": "senha123"}, follow_redirects=True)
    assert "Já existe uma conta" in response.get_data(as_text=True)


def test_trocar_senha(client):
    register(client)
    login(client)
    curta = client.post("/conta", data={"acao": "senha", "senha_atual": "senha123", "nova_senha": "abc123", "confirmar_senha": "abc123"}, follow_redirects=True)
    assert "pelo menos 8" in curta.get_data(as_text=True)
    diferente = client.post("/conta", data={"acao": "senha", "senha_atual": "senha123", "nova_senha": "outra123", "confirmar_senha": "outra124"}, follow_redirects=True)
    assert "não confere" in diferente.get_data(as_text=True)
    ok = client.post("/conta", data={"acao": "senha", "senha_atual": "senha123", "nova_senha": "outra123", "confirmar_senha": "outra123"}, follow_redirects=True)
    assert b"Senha alterada" in ok.data
    client.post("/logout")
    assert "Olá, Maria" in login(client, password="outra123").get_data(as_text=True)
    client.post("/logout")
    assert "inválidos" in login(client, password="senha123").get_data(as_text=True)


def test_checklist(client, app):
    from app.models import item
    register(client)
    login(client)
    nova(client, "Viagem")
    client.post("/tarefas/1/itens", data={"texto": "Passaporte"})
    client.post("/tarefas/1/itens", data={"texto": "Carregador"})
    client.post("/tarefas/1/itens", data={"texto": "  "})
    with app.app_context():
        assert [i["texto"] for i in item.listar(1)] == ["Passaporte", "Carregador"]
    client.post("/tarefas/1/itens/1/feito", data={"feito": "1"})
    response = client.get("/tarefas/")
    assert b"1/2" in response.data
    assert b"Passaporte" in client.get("/tarefas/1/editar").data
    client.post("/tarefas/1/itens/2/excluir")
    with app.app_context():
        assert len(item.listar(1)) == 1
    client.post("/tarefas/1/excluir")
    with app.app_context():
        assert item.listar(1) == []


def test_checklist_de_outro_usuario_e_protegido(client):
    register(client, "Ana", "ana@email.com")
    login(client, "ana@email.com")
    nova(client, "Da Ana")
    client.post("/tarefas/1/itens", data={"texto": "Segredo"})
    client.post("/logout")
    register(client, "Bruno", "bruno@email.com")
    login(client, "bruno@email.com")
    assert client.post("/tarefas/1/itens", data={"texto": "Invasão"}).status_code == 404
    assert client.post("/tarefas/1/itens/1/excluir").status_code == 404


def test_checklist_pela_lista_volta_para_a_lista(client, app):
    from app.models import item
    register(client)
    login(client)
    nova(client, "Mercado")
    resposta = client.post("/tarefas/1/itens", data={"texto": "Leite", "next": "lista"})
    assert resposta.headers["Location"].endswith("/tarefas/")
    lista = client.get("/tarefas/").get_data(as_text=True)
    assert "Leite" in lista and "0/1" in lista
    resposta = client.post("/tarefas/1/itens/1/feito", data={"feito": "1", "next": "lista"})
    assert resposta.headers["Location"].endswith("/tarefas/")
    assert "1/1" in client.get("/tarefas/").get_data(as_text=True)


def test_regras_de_senha(client):
    from app.models.user import validar_senha
    assert "8 caracteres" in validar_senha("abc123")
    assert "letras e números" in validar_senha("somenteletras")
    assert "letras e números" in validar_senha("12345678")
    assert validar_senha("senha123") is None
    resposta = client.post("/cadastro", data={"nome": "Ana", "email": "ana@email.com", "senha": "12345678"}, follow_redirects=True)
    assert "letras e números" in resposta.get_data(as_text=True)
