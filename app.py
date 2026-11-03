"""Interface da lista híbrida: inserção, busca e visualização."""

from inspect import getsource
from textwrap import dedent

import streamlit as st

from logica import ListaHibrida, busca_binaria, busca_sequencial

st.set_page_config(page_title="Lista híbrida", layout="wide", initial_sidebar_state="collapsed")

# A lista permanece salva quando o Streamlit atualiza a página.
if "lista" not in st.session_state:
    st.session_state.lista = ListaHibrida(semente=42)
if "aviso" not in st.session_state:
    st.session_state.aviso = None
if "resultado" not in st.session_state:
    st.session_state.resultado = None

lista = st.session_state.lista

# Cabeçalho e reinício (semente fixa, sem barra lateral).
titulo, acao = st.columns([5, 1], vertical_alignment="center")
with titulo:
    st.title("Lista híbrida")
with acao:
    if st.button("Reiniciar lista", use_container_width=True):
        st.session_state.lista = ListaHibrida(semente=42)
        st.session_state.aviso = None
        st.session_state.resultado = None
        st.rerun()

# Resumo do estado da lista (rótulos e números centralizados).
c1, c2, c3 = st.columns(3)
c1.markdown(f"<div style='text-align:center'>Região ordenada<br><span style='font-size:2rem'>{len(lista.ordenada)}</span></div>", unsafe_allow_html=True)
c2.markdown(f"<div style='text-align:center'>Cauda não ordenada<br><span style='font-size:2rem'>{len(lista.cauda)} / 10</span></div>", unsafe_allow_html=True)
c3.markdown(f"<div style='text-align:center'>Total de chaves<br><span style='font-size:2rem'>{len(lista.ordenada) + len(lista.cauda)}</span></div>", unsafe_allow_html=True)

# Entradas e ações principais.
insercao, busca = st.columns(2, gap="large")
with insercao:
    with st.container(border=True):
        st.subheader("Inserir chave")
        nova_chave = st.number_input("Número inteiro", step=1, value=0, key="inserir")
        if st.button("Inserir na cauda", type="primary", use_container_width=True):
            st.session_state.aviso = lista.inserir(nova_chave)
            st.session_state.resultado = None
            st.rerun()  # Atualiza imediatamente as três métricas.

with busca:
    with st.container(border=True):
        st.subheader("Buscar chave")
        chave = st.number_input("Número procurado", step=1, value=0, key="buscar")
        if st.button("Executar busca", use_container_width=True):
            st.session_state.resultado = lista.buscar(chave)
            st.session_state.aviso = None
            st.rerun()

if st.session_state.aviso is not None:
    sucesso, mensagem = st.session_state.aviso
    (st.success if sucesso else st.warning)(mensagem)

if st.session_state.resultado is not None:
    resultado = st.session_state.resultado
    with st.container(border=True):
        st.subheader("Resultado da busca")
        if resultado["indice"] is None:
            st.write("Chave não encontrada.")
        else:
            st.write(f"**Local:** {resultado['local']} | **Índice:** {resultado['indice']}")

        b, s, t = st.columns(3)
        b.metric("Iterações binárias", resultado["binaria"])
        s.metric("Iterações sequenciais", resultado["sequencial"])
        t.metric("Total de iterações", resultado["total"])

        with st.expander("Ver valores comparados"):
            st.write("**Busca binária:**", " → ".join(
                f"{i}:{v}" for i, v in resultado["passos_binaria"]
            ) or "Não executada")
            st.write("**Busca sequencial:**", " → ".join(
                f"{i}:{v}" for i, v in resultado["passos_sequencial"]
            ) or "Não necessária")
            st.caption("Cada etapa mostra índice:valor. Os índices começam em zero.")

# Duas regiões visualizadas lado a lado.
st.subheader("Estrutura da lista")
ordenada, cauda = st.columns(2, gap="large")
with ordenada:
    st.markdown("**Região ordenada**")
    st.dataframe(
        {"Índice": list(range(len(lista.ordenada))), "Chave": lista.ordenada},
        hide_index=True,
        use_container_width=True,
        height=350,
    )
with cauda:
    st.markdown("**Cauda não ordenada**")
    st.dataframe(
        {
            "Posição": list(range(1, 11)),
            "Chave": [str(v) for v in lista.cauda] + ["—"] * (10 - len(lista.cauda)),
        },
        hide_index=True,
        use_container_width=True,
        height=350,
    )

# Consulta dos componentes: o código exibido vem dos arquivos reais do projeto.
# A seção permanece fechada para não atrapalhar o uso normal da aplicação.
with st.expander("Componentes utilizados e trechos de código"):
    st.write("Selecione um componente para consultar sua função e o código comentado.")
    componentes = {
        "Geração da região ordenada": (
            "Gera 1.024 inteiros distintos com semente fixa e começa com cauda vazia.",
            ListaHibrida.__init__, "logica.py",
        ),
        "Inserção na cauda": (
            "Rejeita chaves repetidas e intercala automaticamente na décima inserção.",
            ListaHibrida.inserir, "logica.py",
        ),
        "Busca binária": (
            "Busca somente na região ordenada, reduzindo o intervalo pela metade.",
            busca_binaria, "logica.py",
        ),
        "Busca sequencial": (
            "Percorre os números da cauda um de cada vez, na ordem de entrada.",
            busca_sequencial, "logica.py",
        ),
        "Busca híbrida e contadores": (
            "Tenta a busca binária primeiro e, se não achar, usa a sequencial; contabiliza os passos.",
            ListaHibrida.buscar, "logica.py",
        ),
        "Ordenação e intercalação": (
            "Ordena a cauda, combina as duas regiões em ordem crescente e esvazia a cauda.",
            ListaHibrida.intercalar, "logica.py",
        ),
    }
    nome = st.selectbox("Componente", list(componentes))
    explicacao, funcao, arquivo = componentes[nome]
    st.write(explicacao)
    st.caption(f"Trecho real de {arquivo}")
    st.code(dedent(getsource(funcao)), language="python")
