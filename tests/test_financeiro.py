import pandas as pd
import pytest
from financeiro import validar_transacoes, resumo, despesas_por_categoria, dicas


def exemplo():
    return pd.DataFrame({"data": ["2026-01-02", "2026-01-03", "2026-01-04"],
                         "descricao": ["Salário", "Mercado", "Ônibus"],
                         "categoria": ["Salário", "Alimentação", "Transporte"],
                         "tipo": ["receita", "despesa", "despesa"],
                         "valor": [2000, 300, 100]})


def test_resumo_e_categorias():
    df = validar_transacoes(exemplo())
    assert resumo(df) == {"receitas": 2000., "despesas": 400., "saldo": 1600., "taxa_poupanca": 0.8}
    assert despesas_por_categoria(df).iloc[0]["categoria"] == "Alimentação"
    assert len(dicas(df, limite_mensal=200)) == 3


def test_entrada_invalida():
    df = exemplo()
    df.loc[0, "valor"] = -1
    with pytest.raises(ValueError):
        validar_transacoes(df)


def test_tipo_invalido():
    df = exemplo()
    df.loc[0, "tipo"] = "transferência"
    with pytest.raises(ValueError):
        validar_transacoes(df)


def test_sem_receita():
    df = validar_transacoes(exemplo().iloc[1:])
    assert resumo(df)["taxa_poupanca"] == 0
    assert resumo(df)["saldo"] == -400
