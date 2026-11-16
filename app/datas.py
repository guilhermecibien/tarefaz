from datetime import date

DIAS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def rotulo_prazo(prazo, hoje=None):
    """Texto curto para exibir um prazo (AAAA-MM-DD) em relação a hoje."""
    if not prazo:
        return ""
    hoje = hoje or date.today()
    dia = date.fromisoformat(prazo)
    diff = (dia - hoje).days
    if diff == 0:
        return "Hoje"
    if diff == 1:
        return "Amanhã"
    if diff == -1:
        return "Ontem"
    if -30 <= diff < 0:
        return f"há {-diff} dias"
    if 2 <= diff <= 6:
        return DIAS[dia.weekday()]
    if dia.year == hoje.year:
        return dia.strftime("%d/%m")
    return dia.strftime("%d/%m/%Y")
