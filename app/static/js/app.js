document.querySelectorAll('[data-confirm]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});

window.setTimeout(() => document.querySelectorAll('.alert').forEach((item) => item.remove()), 4500);

// ---------- atalhos de data ----------

function dataLocal(dias) {
  const d = new Date();
  d.setDate(d.getDate() + dias);
  const mes = String(d.getMonth() + 1).padStart(2, '0');
  const dia = String(d.getDate()).padStart(2, '0');
  return `${d.getFullYear()}-${mes}-${dia}`;
}

document.querySelectorAll('.atalhos').forEach((grupo) => {
  const campo = grupo.parentElement.querySelector('input[type=date]');
  const marcar = () => grupo.querySelectorAll('button').forEach((b) => {
    b.classList.toggle('ativo', campo.value === dataLocal(Number(b.dataset.dias)));
  });
  grupo.querySelectorAll('button').forEach((botao) => {
    botao.addEventListener('click', () => {
      const valor = dataLocal(Number(botao.dataset.dias));
      campo.value = campo.value === valor ? '' : valor;
      marcar();
    });
  });
  campo.addEventListener('input', marcar);
  marcar();
});

// ---------- lista de tarefas ----------

function iniciarLinha(linha) {
  // concluir a tarefa
  const caixa = linha.querySelector('.check-form input[type=checkbox]');
  caixa.addEventListener('change', () => {
    fetch(caixa.form.action, { method: 'POST', body: new FormData(caixa.form) })
      .then(() => window.location.reload());
  });

  // abrir e fechar o checklist
  const botao = linha.querySelector('.chk-toggle');
  botao.addEventListener('click', () => {
    const aberto = linha.classList.toggle('aberto');
    botao.setAttribute('aria-expanded', aberto);
    if (aberto) linha.querySelector('.novo-item input').focus();
  });

  // editar o título no lugar
  const bloco = linha.querySelector('.titulo');
  const texto = bloco.querySelector('.texto');
  texto.addEventListener('click', () => {
    if (bloco.querySelector('input.edita')) return;
    const original = texto.textContent;
    const campo = document.createElement('input');
    campo.className = 'edita';
    campo.value = original;
    texto.hidden = true;
    texto.after(campo);
    campo.focus();
    campo.select();

    let encerrado = false;
    const fechar = () => { encerrado = true; campo.remove(); texto.hidden = false; };

    const salvar = () => {
      if (encerrado) return;
      const novo = campo.value.trim();
      if (!novo || novo === original) return fechar();
      const dados = new FormData();
      dados.append('titulo', novo);
      fetch(bloco.dataset.url, { method: 'POST', body: dados })
        .then((r) => r.json().then((j) => ({ ok: r.ok, j })))
        .then(({ ok, j }) => {
          if (ok) texto.textContent = j.titulo;
          fechar();
        })
        .catch(fechar);
    };

    campo.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') { e.preventDefault(); salvar(); }
      if (e.key === 'Escape') fechar();
    });
    campo.addEventListener('blur', salvar);
  });
}

document.querySelectorAll('.item').forEach(iniciarLinha);

// itens do checklist na própria lista: troca só a linha da tarefa
function enviarItemNaLista(form) {
  const linha = form.closest('.item');
  const digitando = form.classList.contains('novo-item');
  fetch(form.action, { method: 'POST', body: new FormData(form) })
    .then((r) => r.text())
    .then((html) => {
      const nova = new DOMParser().parseFromString(html, 'text/html').getElementById(linha.id);
      if (!nova) return window.location.reload();
      nova.classList.add('aberto');
      linha.replaceWith(nova);
      iniciarLinha(nova);
      nova.querySelector('.chk-toggle').setAttribute('aria-expanded', true);
      if (digitando) nova.querySelector('.novo-item input').focus();
    });
}

document.addEventListener('submit', (e) => {
  if (!e.target.closest('.painel')) return;
  e.preventDefault();
  enviarItemNaLista(e.target);
});

document.addEventListener('change', (e) => {
  if (e.target.type === 'checkbox' && e.target.closest('.painel')) enviarItemNaLista(e.target.form);
});

// ---------- checklist na página de edição ----------

const checklist = document.getElementById('checklist');
if (checklist) {
  const enviar = (form) => {
    fetch(form.action, { method: 'POST', body: new FormData(form) })
      .then((r) => r.text())
      .then((html) => {
        const novo = new DOMParser().parseFromString(html, 'text/html').getElementById('checklist');
        if (!novo) return;
        const digitando = form.classList.contains('novo-item');
        checklist.innerHTML = novo.innerHTML;
        if (digitando) checklist.querySelector('.novo-item input').focus();
      });
  };
  checklist.addEventListener('submit', (e) => {
    e.preventDefault();
    enviar(e.target);
  });
  checklist.addEventListener('change', (e) => {
    if (e.target.type === 'checkbox') enviar(e.target.form);
  });
}

// ---------- tema claro/escuro ----------

const botaoTema = document.getElementById('tema');
if (botaoTema) {
  const escuroAgora = () => {
    const t = document.documentElement.dataset.theme;
    return t ? t === 'dark' : window.matchMedia('(prefers-color-scheme: dark)').matches;
  };
  const rotular = () => { botaoTema.textContent = escuroAgora() ? 'Claro' : 'Escuro'; };
  botaoTema.addEventListener('click', () => {
    const novo = escuroAgora() ? 'light' : 'dark';
    document.documentElement.dataset.theme = novo;
    try { localStorage.setItem('tema', novo); } catch (e) {}
    rotular();
  });
  rotular();
}
