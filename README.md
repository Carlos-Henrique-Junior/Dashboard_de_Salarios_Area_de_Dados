Análise de Salários no Mercado de Dados

📄 Sobre o Projeto
Este projeto apresenta uma análise exploratória detalhada sobre os salários no mercado de dados. O objetivo principal é investigar a distribuição salarial e entender como fatores determinantes — como nível de senioridade, tipo de emprego, localização e tamanho da empresa — influenciam a remuneração dos profissionais da área.

Este notebook é um excelente ponto de partida para quem busca compreender as tendências salariais e os fatores que moldam a compensação no crescente campo de dados.

## 🚀 Como Executar o Dashboard

O projeto inclui um dashboard interativo em Streamlit (`app.py`) que consome o conjunto de dados limpo `dados-imersao-final.csv` (versão local, sem dependência de rede).

1. Instale as dependências:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Execute o dashboard:

```bash
streamlit run app.py
```

Para rodar os testes automatizados (verificação de execução do app e contrato dos dados), após instalar as dependências do projeto:

```bash
pip install -r requirements-dev.txt
pytest
```

📓 Conteúdo do Notebook
A análise foi estruturada em etapas claras, desde a importação até a visualização dos insights:

Carregamento e Inspeção Inicial dos Dados:

Importação do conjunto de dados de salários.

Verificação inicial da estrutura, tipos de dados e informações gerais do dataset.

Limpeza e Preparação dos Dados:

Renomeação de Colunas: As colunas foram traduzidas para o português brasileiro para maior clareza.

Tradução de Categorias: Os valores das colunas senioridade, contrato, remoto e tamanho_empresa foram padronizados e traduzidos.

Tratamento de Valores Ausentes: Remoção de registros com dados nulos para garantir a qualidade da análise.

Conversão de Tipos de Dados: Ajuste das colunas ano e salario para os tipos numéricos corretos.

Análise Exploratória e Visualização:

Distribuição Geral de Salários: Visualização da distribuição dos salários em USD através de histogramas e boxplots.

Análise por Senioridade: Investigação da média e da dispersão salarial entre os diferentes níveis de senioridade (Entry-level, Mid-level, Senior, Executive).

Análise por Tipo de Trabalho: Gráfico de pizza para mostrar a proporção de cada modalidade de contrato (integral, meio período, etc.).

Salários de Cientistas de Dados por País: Análise comparativa da média salarial para a função de Cientista de Dados em diferentes países, apresentada em gráficos de barras e em um mapa coroplético interativo.

Exportação dos Dados Limpos:

O DataFrame final, após todo o processo de limpeza e tratamento, é exportado para um novo arquivo CSV, pronto para futuras análises.

🛠️ Ferramentas Utilizadas
As seguintes bibliotecas Python foram utilizadas para a realização deste projeto:

Pandas: Para manipulação e análise de dados.

Matplotlib e Seaborn: Para a criação de gráficos estáticos e visualizações estatísticas.

Plotly Express: Para a criação de visualizações interativas, como o mapa coroplético.

pycountry: Para a conversão de códigos de países (ISO 2 para ISO 3), permitindo a plotagem geográfica.
