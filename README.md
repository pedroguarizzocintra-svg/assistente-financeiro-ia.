# 💸 FinIA — Assistente Virtual de Finanças com IA

Projeto de portfólio desenvolvido como **nova implementação demonstrativa**, inspirado em um projeto integrador acadêmico sobre um assistente financeiro com inteligência artificial. A aplicação ajuda a visualizar receitas e despesas, organizar categorias, acompanhar o orçamento e conversar com uma IA opcional sobre o resumo financeiro.

> **Aviso:** projeto educacional. Não oferece consultoria financeira, contábil ou recomendações personalizadas de investimento.

## Funcionalidades

- Cadastro de receitas e despesas e importação/exportação em CSV.
- Indicadores de receitas, despesas e saldo; filtro por período.
- Gráfico de despesas por categoria e alertas básicos de orçamento.
- Chat de IA opcional via API da OpenAI, com modo informativo sem API.
- Dados mantidos apenas na sessão do Streamlit; não há banco de dados nem login.

## Tecnologias

Python · Streamlit · Pandas · API da OpenAI (opcional) · Pytest.

## Como executar

~~~bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
~~~

Abra o endereço local indicado no terminal. Use `dados/exemplo.csv` para testar com informações fictícias.

### Ativar o chat com IA (opcional)

Defina a variável de ambiente `OPENAI_API_KEY` com uma chave da API da OpenAI. A API pode ter custos próprios. No PowerShell:

~~~powershell
$env:OPENAI_API_KEY="sua_chave"
streamlit run app.py
~~~

O nome do modelo pode ser alterado por `OPENAI_MODEL`. **Nunca envie a chave de API ao GitHub.** Sem chave, as métricas e dicas locais continuam disponíveis.

## Formato do CSV

As colunas exigidas são `data,descricao,categoria,tipo,valor`. Use datas `AAAA-MM-DD`, valor numérico positivo com ponto decimal e `tipo` igual a `receita` ou `despesa`.

## Testes

~~~bash
python -m pytest -q
~~~

## Organização

~~~text
app.py                 # Interface e conversa com IA
financeiro.py          # Cálculos e validações financeiras
requirements.txt       # Dependências Python
dados/exemplo.csv       # Movimentações fictícias
tests/test_financeiro.py
.env.example            # Referência de configuração
~~~

## Sobre o desenvolvimento

Esta é uma **recriação para portfólio**, e não o código-fonte original do projeto acadêmico. Os dados do exemplo são fictícios. A publicação como projeto acadêmico em equipe deve identificar as contribuições reais dos participantes quando aplicável.

Autor do portfólio: Pedro Guarizzo Cintra.
