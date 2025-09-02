import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Monitoramento IA Piauí", page_icon="🤖", layout="wide")

# Título do dashboard
st.title("🤖 Monitoramento de Percepção sobre IA no Piauí")
st.markdown("---")

# Carregar dados processados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed_news.csv')
        return df
    except FileNotFoundError:
        st.error("Arquivo de dados não encontrado. Execute primeiro o processamento.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Sidebar com filtros
st.sidebar.header("Filtros")
sentimento_filter = st.sidebar.multiselect(
    "Filtrar por Sentimento:",
    options=df['sentiment'].unique(),
    default=df['sentiment'].unique()
)

# Aplicar filtros
df_filtered = df[df['sentiment'].isin(sentimento_filter)]

# Métricas principais
st.header("📊 Métricas Gerais")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total de Notícias", len(df_filtered))
with col2:
    st.metric("Notícias Positivas", len(df_filtered[df_filtered['sentiment'] == 'positivo']))
with col3:
    st.metric("Notícias Negativas", len(df_filtered[df_filtered['sentiment'] == 'negativo']))

# Gráfico de Pizza - Distribuição de Sentimentos
st.header("📈 Distribuição de Sentimentos")
fig_pizza = px.pie(
    df_filtered, 
    names='sentiment', 
    title='Proporção de Sentimentos'
)
st.plotly_chart(fig_pizza, use_container_width=True)

# Combine título e descrição
df_filtered['texto_completo'] = df_filtered['title'].astype(str) + ' ' + df_filtered['description'].astype(str)
all_text = ' '.join(df_filtered['texto_completo'].dropna())
if all_text.strip():
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)
else:
    st.warning("Não há texto suficiente para gerar nuvem de palavras.")

# Tabela com as notícias
st.header("📰 Notícias Analisadas")
for _, row in df_filtered.iterrows():
    with st.expander(f"{row['title']} - {row['sentiment']}"):
        st.write(f"**Descrição:** {row['description']}")
        st.write(f"**Sentimento:** {row['sentiment']}")
        st.write(f"**Link:** [Ver notícia](#)")  # Adicione os links reais depois

# Rodapé com aviso de limitações - ADICIONE ISSO NO FINAL DO ARQUIVO
st.markdown("---")
st.warning("""
**⚠️ Limitações do Modelo:** 
Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos. 
Os resultados devem ser interpretados com cautela.
""")