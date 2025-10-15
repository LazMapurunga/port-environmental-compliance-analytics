import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Título do dashboard
st.title("🚢 Port Environmental Compliance Dashboard")
st.markdown("**Real audit data from Port of Fortaleza - September 2025**")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('audit_compliance_data_2025.csv')
    return df

df = load_data()

# KPIs principais
col1, col2, col3, col4 = st.columns(4)

total_items = len(df)
conforme = len(df[df['CLASSIFICAÇÃO'] == 'Conforme'])
compliance_rate = (conforme / total_items) * 100

col1.metric("Total Itens", total_items)
col2.metric("Conformidade", f"{compliance_rate:.1f}%", f"{conforme} itens")
col3.metric("Alto Risco", len(df[df['IMPACTO RISCO'] == 'Alto']))
col4.metric("Em Andamento", len(df[df['STATUS IMPLEMENTAÇÃO'] == 'Em Andamento']))

# Gráfico de conformidade (Gauge)
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number+delta",
    value = compliance_rate,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Taxa de Conformidade (%)"},
    delta = {'reference': 60, 'increasing': {'color': "green"}},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 60], 'color': "lightgray"},
            {'range': [60, 85], 'color': "yellow"},
            {'range': [85, 100], 'color': "lightgreen"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90
        }
    }
))

st.plotly_chart(fig_gauge, use_container_width=True)

# Distribuição por classificação
fig_pie = px.pie(
    values=[26, 9, 1, 1],
    names=['Conforme', 'Oportunidade', 'Não Conformidade', 'Observação'],
    title='Distribuição das Classificações',
    color_discrete_sequence=['green', 'orange', 'red', 'blue']
)
st.plotly_chart(fig_pie, use_container_width=True)

# Mostrar dados
if st.checkbox("Mostrar dados brutos"):
    st.dataframe(df)
