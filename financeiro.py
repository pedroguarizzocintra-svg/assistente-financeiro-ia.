"""Funções de análise financeira; não exigem conexão à internet."""
from __future__ import annotations
import pandas as pd

CATEGORIAS = ["Alimentação", "Moradia", "Transporte", "Educação", "Saúde", "Lazer", "Outros"]
COLUNAS = ["data", "descricao", "categoria", "tipo", "valor"]


def validar_transacoes(df: pd.DataFrame) -> pd.DataFrame:
    """Valida CSV de lançamentos; valores são sempre positivos e tipo define o fluxo."""
    ausentes = [c for c in COLUNAS if c not in df.columns]
    if ausentes:
        raise ValueError("Colunas ausentes: " + ", ".join(ausentes))
    resultado = df[COLUNAS].copy()
    resultado["data"] = pd.to_datetime(resultado["data"], errors="coerce")
    resultado["valor"] = pd.to_numeric(resultado["valor"], errors="coerce")
    resultado["tipo"] = resultado["tipo"].astype(str).str.strip().str.lower()
    resultado["categoria"] = resultado["categoria"].astype(str).str.strip()
    resultado["descricao"] = resultado["descricao"].astype(str).str.strip()
    if resultado["data"].isna().any():
        raise ValueError("A coluna 'data' precisa conter datas válidas (AAAA-MM-DD).")
    if resultado["valor"].isna().any() or (resultado["valor"] <= 0).any():
        raise ValueError("A coluna 'valor' precisa conter números positivos.")
    if not resultado["tipo"].isin(["receita", "despesa"]).all():
        raise ValueError("A coluna 'tipo' aceita apenas 'receita' ou 'despesa'.")
    if (resultado["categoria"] == "").any() or (resultado["descricao"] == "").any():
        raise ValueError("Descrição e categoria não podem estar vazias.")
    return resultado.sort_values("data").reset_index(drop=True)


def resumo(df: pd.DataFrame) -> dict[str, float]:
    receita = float(df.loc[df["tipo"] == "receita", "valor"].sum())
    despesa = float(df.loc[df["tipo"] == "despesa", "valor"].sum())
    return {"receitas": receita, "despesas": despesa, "saldo": receita - despesa,
            "taxa_poupanca": (receita - despesa) / receita if receita > 0 else 0.0}


def despesas_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    return (df.loc[df["tipo"] == "despesa"].groupby("categoria", as_index=False)["valor"]
            .sum().sort_values("valor", ascending=False))


def dicas(df: pd.DataFrame, limite_mensal: float | None = None) -> list[str]:
    info = resumo(df)
    respostas = []
    if info["despesas"] > info["receitas"]:
        respostas.append("Suas despesas superam suas receitas no período selecionado. Reveja primeiro os gastos ajustáveis.")
    elif info["receitas"] > 0:
        respostas.append(f"Sua taxa de poupança no período é {info['taxa_poupanca']:.1%}.")
    por_categoria = despesas_por_categoria(df)
    if not por_categoria.empty:
        maior = por_categoria.iloc[0]
        respostas.append(f"Sua maior categoria de gastos é {maior['categoria']}: R$ {maior['valor']:,.2f}.")
    if limite_mensal is not None and limite_mensal > 0 and info["despesas"] > limite_mensal:
        respostas.append("Suas despesas ultrapassaram o orçamento definido para o período selecionado.")
    if not respostas:
        respostas.append("Adicione movimentações para receber um diagnóstico financeiro.")
    return respostas
