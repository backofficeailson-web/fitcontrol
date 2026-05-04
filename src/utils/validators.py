from datetime import date

def calcular_status_vencimento(vencimento):
    hoje = date.today()
    try:
        dia = int(str(vencimento).strip())
        if not 1 <= dia <= 31:
            raise ValueError
    except (ValueError, TypeError):
        return {"status": "data_invalida", "prox_venc": "Inválido", "dias_rest": "?"}

    try:
        prox = date(hoje.year, hoje.month, dia)
        if prox < hoje:
            if hoje.month == 12:
                prox = date(hoje.year + 1, 1, dia)
            else:
                prox = date(hoje.year, hoje.month + 1, dia)
    except ValueError:
        return {"status": "data_invalida", "prox_venc": "Inválido", "dias_rest": "?"}

    diff = (prox - hoje).days
    if diff < 0:
        status = "vencido"
    elif diff <= 5:
        status = "proximo"
    else:
        status = "em_dia"

    return {
        "status": status,
        "prox_venc": prox.strftime("%d/%m/%Y"),
        "dias_rest": diff
    }
