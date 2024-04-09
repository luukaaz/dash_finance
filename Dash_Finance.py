#Importação de Bibliotecas
import streamlit as st


st.title('Início')

st.markdown('---')

st.page_link("pages/Indicadores.py", label="Ver Indicadores", icon="📊")

st.page_link("pages/Mercado.py", label="Ir para Mercados", icon="💰")

st.page_link("pages/Valuation_FIIs.py", label="Avaliar um Fundo Imobiliário", icon="🏢")

