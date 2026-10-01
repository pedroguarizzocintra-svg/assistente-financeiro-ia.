"""Dashboard de finanças pessoais com chat de IA opcional."""
import os
import pandas as pd
import streamlit as st
from financeiro import COLUNAS, validar_transacoes, resumo, despesas_por_categoria, dicas

st.set_page_config(page_title="FinIA | Assistente Financeiro", page_icon="💸", layout="wide")
st.title("💸 FinIA — Assistente Financeiro")
st.caption("Projeto demonstrativo de educação financeira • dados tratados apenas nesta sessão")

if "movimentos" not in st.session_state:
    st.session_state.movimentos = pd.DataFrame(columns=COLUNAS)

with st.sidebar:
    st.header("Seus dados")
    arquivo = st.file_uploader("Importar lançamentos (CSV)", type="csv")
    if arquivo is not None and st.button("Importar CSV", use_container_width=True):
        try:
            st.session_state.movimentos = validar_transacoes(pd.read_csv(arquivo))
            st.success("Dados importados com sucesso.")
        except (ValueError, pd.errors.ParserError, UnicodeDecodeError) as erro:
            st.error(str(erro))
    orcamento = st.number_input("Orçamento do período (R$)", min_value=0.0, value=1500.0, step=50.0)
    st.caption("Use apenas dados fictícios ou dados que você tenha autorização para processar.")

with st.expander("➕ Adicionar lançamento"):
    with st.form("lancamento", clear_on_submit=True):
        data = st.date_input("Data")
        descricao = st.text_input("Descrição")
        categoria = st.selectbox("Categoria", ["Alimentação", "Moradia", "Transporte", "Educação", "Saúde", "Lazer", "Outros", "Salário", "Freelance"])
        tipo = st.selectbox("Tipo", ["despesa", "receita"])
        valor = st.number_input("Valor (R$)", min_value=0.01, value=10.0, step=1.0)
        if st.form_submit_button("Salvar lançamento"):
            if not descricao.strip():
                st.error("Informe uma descrição.")
            else:
                novo = pd.DataFrame([[str(data), descricao.strip(), categoria, tipo, valor]], columns=COLUNAS)
                st.session_state.movimentos = validar_transacoes(pd.concat([st.session_state.movimentos, novo], ignore_index=True))
                st.success("Lançamento salvo nesta sessão.")

df = st.session_state.movimentos
if df.empty:
    st.info("Comece adicionando um lançamento ou importando o arquivo dados/exemplo.csv.")
else:
    inicio = df["data"].min().date()
    fim = df["data"].max().date()
    periodo = st.date_input("Período analisado", value=(inicio, fim))
    if isinstance(periodo, tuple) and len(periodo) == 2:
        df = df.loc[df["data"].dt.date.between(periodo[0], periodo[1])].copy()
    info = resumo(df)
    c1, c2, c3 = st.columns(3)
    c1.metric("Receitas", f"R$ {info['receitas']:,.2f}")
    c2.metric("Despesas", f"R$ {info['despesas']:,.2f}")
    c3.metric("Saldo", f"R$ {info['saldo']:,.2f}")
    categorias = despesas_por_categoria(df)
    if not categorias.empty:
        st.subheader("Despesas por categoria")
        st.bar_chart(categorias.set_index("categoria")["valor"])
    st.subheader("Diagnóstico")
    for dica in dicas(df, orcamento):
        st.write("• " + dica)
    st.subheader("Lançamentos")
    st.dataframe(df, use_container_width=True, hide_index=True)
    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("Exportar CSV", data=csv, file_name="minhas_financas.csv", mime="text/csv")

st.divider()
st.subheader("🤖 Converse com o FinIA")
st.caption("Opcional: defina OPENAI_API_KEY no ambiente. Não informe senhas, CPF ou dados bancários no chat.")
if "chat" not in st.session_state:
    st.session_state.chat = []
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
pergunta = st.chat_input("Ex.: Onde estão meus maiores gastos?")
if pergunta:
    st.session_state.chat.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.write(pergunta)
    info = resumo(df)
    contexto = (f"Resumo da seleção: receitas R$ {info['receitas']:.2f}, "
                f"despesas R$ {info['despesas']:.2f}, saldo R$ {info['saldo']:.2f}. "
                f"Despesas por categoria: {despesas_por_categoria(df).to_dict('records')}.")
    chave = os.environ.get("OPENAI_API_KEY")
    if chave:
        try:
            from openai import OpenAI
            resposta = OpenAI(api_key=chave).responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                instructions=("Você é um assistente didático de finanças pessoais. Responda em português, "
                              "use somente o resumo fornecido, não invente transações, não recomende investimentos "
                              "específicos e não peça dados sensíveis. Informe que o conteúdo é educativo."),
                input=contexto + "\nPergunta do usuário: " + pergunta,
            ).output_text
        except Exception:
            resposta = "Não foi possível consultar a IA. Confira sua chave, conexão e acesso ao modelo.\n\n" + "\n".join(dicas(df, orcamento))
    else:
        resposta = "Modo sem IA: configure OPENAI_API_KEY para conversas livres.\n\n" + "\n".join(dicas(df, orcamento))
    with st.chat_message("assistant"):
        st.write(resposta)
    st.session_state.chat.append({"role": "assistant", "content": resposta})
