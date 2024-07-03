# Importa a biblioteca Streamlit, que é utilizada para criar aplicativos web interativos em Python
import streamlit as st

# Define o título da página inicial do aplicativo
st.title('Início')  

# Adiciona uma linha horizontal como separador
st.markdown('---')

# Cria um link para a página de Indicadores Econômicos com o rótulo "Ver Indicadores Econômicos" e um ícone de dinheiro
st.page_link("pages/Economia.py", label="Ver Indicadores Econômicos", icon="💰")

# Cria um link para a página de Indicadores de Empresas Brasileiras com o rótulo "Ver Indicadores de Empresas Brasileiras" e um ícone de gráfico
st.page_link("pages/Indicadores.py", label="Ver Indicadores de Empresas Brasileiras", icon="📊")

# Cria um link para a página de Mercados Mundiais com o rótulo "Ir para Mercados Mundiais" e um ícone de globo
st.page_link("pages/Mercado.py", label="Ir para Mercados Mundiais", icon="🌐")

# Cria um link para a página de Valuation de Fundos Imobiliários com o rótulo "Avaliar um Fundo Imobiliário" e um ícone de prédio
st.page_link("pages/Valuation_FIIs.py", label="Avaliar um Fundo Imobiliário", icon="🏢")

