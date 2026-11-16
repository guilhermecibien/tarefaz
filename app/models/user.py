from werkzeug.security import check_password_hash, generate_password_hash

from app.models.database import get_db


def validar_senha(senha):
    """Devolve a mensagem de erro, ou None se a senha for aceitável."""
    if len(senha) < 8:
        return "A senha deve ter pelo menos 8 caracteres."
    if not any(c.isalpha() for c in senha) or not any(c.isdigit() for c in senha):
        return "A senha deve ter letras e números."
    return None


def get_by_email(email):
    return get_db().execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()


def get_by_id(user_id):
    return get_db().execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()


def create(nome, email, senha):
    db = get_db()
    cursor = db.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
        (nome, email.lower().strip(), generate_password_hash(senha)),
    )
    db.commit()
    return cursor.lastrowid


def password_is_valid(user, senha):
    return user is not None and check_password_hash(user["senha_hash"], senha)


def update_profile(user_id, nome, email):
    db = get_db()
    db.execute(
        "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
        (nome, email.lower().strip(), user_id),
    )
    db.commit()


def update_password(user_id, senha):
    db = get_db()
    db.execute("UPDATE usuarios SET senha_hash = ? WHERE id = ?", (generate_password_hash(senha), user_id))
    db.commit()
