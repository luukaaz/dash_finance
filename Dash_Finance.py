import streamlit as st


st.title('Início')  

st.markdown('---')

st.page_link("pages/Economia.py", label="Ver Indicadores Econômicos", icon="💰")

st.page_link("pages/Indicadores.py", label="Ver Indicadores de Ações", icon="📊")

st.page_link("pages/Mercado.py", label="Ir para Mercados Mundiais", icon="🌐")

st.page_link("pages/Valuation_FIIs.py", label="Avaliar um Fundo Imobiliário", icon="🏢")

