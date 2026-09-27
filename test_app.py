import pandas as pd
from streamlit.testing.v1 import AppTest

ARQUIVO_DADOS = "dados-imersao-final.csv"
COLUNAS_ESPERADAS = {
    "ano",
    "senioridade",
    "contrato",
    "cargo",
    "usd",
    "remoto",
    "residencia_iso3",
    "tamanho_empresa",
}


def executar_app():
    at = AppTest.from_file("app.py", default_timeout=300)
    at.run()
    return at


def test_app_executa_sem_excecao():
    at = executar_app()
    assert not at.exception
    assert at.title[0].value == "🎲 Dashboard de Análise de Salários na Área de Dados"
    assert len(at.metric) == 4


def test_contrato_de_dados_do_csv():
    df = pd.read_csv(ARQUIVO_DADOS)
    assert not df.empty
    assert COLUNAS_ESPERADAS.issubset(df.columns)
    for coluna in ["ano", "senioridade", "contrato", "tamanho_empresa"]:
        assert df[coluna].notna().all(), f"Coluna {coluna} contém valores nulos"


def test_filtro_ano_restringe_dados():
    df = pd.read_csv(ARQUIVO_DADOS)
    at = executar_app()
    assert not at.exception
    seletor_ano = at.sidebar.multiselect[0]
    seletor_ano.set_value([2025])
    at.run()
    assert not at.exception
    esperado = (df["ano"] == 2025).sum()
    resultado = at.dataframe[0].value
    assert len(resultado) == esperado
