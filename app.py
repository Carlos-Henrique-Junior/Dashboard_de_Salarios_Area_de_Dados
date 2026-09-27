from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================
st.set_page_config(
    page_title="Dashboard de Salários - Área de Dados",
    page_icon="📊",
    layout="wide",
)

ARQUIVO_DADOS = Path(__file__).with_name("dados-imersao-final.csv")
COLUNAS_FILTRO = ["ano", "senioridade", "contrato", "tamanho_empresa"]

# ================================
# FUNÇÃO PARA CARREGAR DADOS
# ================================
@st.cache_data
def carregar_dados():
    return pd.read_csv(ARQUIVO_DADOS)

# ================================
# FILTROS NA SIDEBAR
# ================================
def aplicar_filtros(data):
    st.sidebar.header("🔍 Filtros")
    filtros = {}
    for coluna in COLUNAS_FILTRO:
        valores = sorted(data[coluna].unique())
        filtros[coluna] = st.sidebar.multiselect(
            coluna.capitalize(), valores, default=valores
        )
    mascara = pd.Series(True, index=data.index)
    for coluna in COLUNAS_FILTRO:
        mascara &= data[coluna].isin(filtros[coluna])
    return data[mascara]

# ================================
# MÉTRICAS PRINCIPAIS
# ================================
def exibir_metricas(data):
    if data.empty:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        return
    salario_medio = data['usd'].mean()
    salario_maximo = data['usd'].max()
    total_registros = len(data)
    cargo_mais_frequente = data['cargo'].mode()[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Salário Médio", f"${salario_medio:,.0f}")
    col2.metric("🏆 Salário Máximo", f"${salario_maximo:,.0f}")
    col3.metric("📊 Total de Registros", f"{total_registros:,}")
    col4.metric("👔 Cargo Mais Frequente", cargo_mais_frequente)

# ================================
# GRÁFICOS
# ================================
def grafico_top_cargos(data):
    top_cargos = data.groupby('cargo')['usd'].mean().nlargest(10).sort_values().reset_index()
    fig = px.bar(
        top_cargos, x='usd', y='cargo', orientation='h',
        title="Top 10 Cargos por Salário Médio",
        labels={'usd': 'Média Salarial (USD)', 'cargo': ''},
        color='usd', color_continuous_scale='Viridis'
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def grafico_distribuicao(data):
    fig = px.histogram(
        data, x='usd', nbins=30,
        title="Distribuição de Salários Anuais",
        labels={'usd': 'Faixa Salarial (USD)'},
        color_discrete_sequence=['#1f77b4']
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def grafico_trabalho_remoto(data):
    remoto_contagem = data['remoto'].value_counts().reset_index()
    remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
    fig = px.pie(
        remoto_contagem, names='tipo_trabalho', values='quantidade',
        title='Proporção dos Tipos de Trabalho',
        hole=0.5, color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

def grafico_salario_por_pais(data):
    df_ds = data[data['cargo'] == 'Data Scientist']
    if df_ds.empty:
        st.info("Nenhum Cientista de Dados nos filtros aplicados.")
        return
    media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index()
    fig = px.choropleth(
        media_ds_pais, locations='residencia_iso3', color='usd',
        color_continuous_scale='RdYlGn',
        title='Salário Médio de Cientista de Dados por País',
        labels={'usd': 'Salário Médio (USD)', 'residencia_iso3': 'País'}
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

# ================================
# APP
# ================================
try:
    df = carregar_dados()
except FileNotFoundError:
    st.error(f"Arquivo de dados não encontrado: {ARQUIVO_DADOS.name}")
    st.stop()
df_filtrado = aplicar_filtros(df)

st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Use os filtros à esquerda para refinar sua análise.")

exibir_metricas(df_filtrado)
st.markdown("---")

if not df_filtrado.empty:
    col1, col2 = st.columns(2)
    with col1: grafico_top_cargos(df_filtrado)
    with col2: grafico_distribuicao(df_filtrado)
    col3, col4 = st.columns(2)
    with col3: grafico_trabalho_remoto(df_filtrado)
    with col4: grafico_salario_por_pais(df_filtrado)
else:
    st.warning("Ajuste os filtros para visualizar os gráficos.")

st.subheader("📄 Dados Detalhados")
st.dataframe(df_filtrado, use_container_width=True)
