import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuração da página
st.set_page_config(
    page_title="🤖 IA Piauí Monitor", 
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {font-size: 2.5rem !important; color: #1f77b4;}
    .metric-card {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
    .positive {color: #2ecc71 !important;}
    .negative {color: #e74c3c !important;}
    .neutral {color: #f39c12 !important;}
</style>
""", unsafe_allow_html=True)

# Título do dashboard
st.markdown('<h1 class="main-header">🤖 Monitoramento de IA no Piauí</h1>', unsafe_allow_html=True)
st.markdown("---")

# Carregar dados
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/processed_news.csv')
        df['data'] = pd.date_range(start='2024-01-01', periods=len(df), freq='D')
        return df
    except:
        # Dados de exemplo se o arquivo não existir
        data = {
            'title': ['Governo do Piauí investe em IA', 'Preocupações com IA', 'Startup de IA cresce'],
            'description': ['Investimento em tecnologia', 'Riscos mencionados', 'Crescimento no mercado'],
            'sentiment': ['positivo', 'negativo', 'positivo'],
            'data': pd.date_range(start='2024-01-01', periods=3, freq='D')
        }
        return pd.DataFrame(data)

df = load_data()

# Sidebar com filtros
st.sidebar.header("🎛️ Filtros Avançados")

# Filtro por sentimento
sentimentos = st.sidebar.multiselect(
    "Filtrar por Sentimento:",
    options=df['sentiment'].unique(),
    default=df['sentiment'].unique()
)

# Filtro por data (se disponível)
if 'data' in df.columns:
    min_date = df['data'].min()
    max_date = df['data'].max()
    date_range = st.sidebar.date_input(
        "Período:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

# Aplicar filtros
df_filtered = df[df['sentiment'].isin(sentimentos)]
if 'data' in df.columns and len(date_range) == 2:
    df_filtered = df_filtered[
        (df_filtered['data'] >= pd.to_datetime(date_range[0])) &
        (df_filtered['data'] <= pd.to_datetime(date_range[1]))
    ]

# Métricas principais
st.header("📊 Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total de Notícias", len(df_filtered))
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    positivas = len(df_filtered[df_filtered['sentiment'] == 'positivo'])
    st.metric("Notícias Positivas", positivas, delta=f"{positivas/len(df_filtered)*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    negativas = len(df_filtered[df_filtered['sentiment'] == 'negativo'])
    st.metric("Notícias Negativas", negativas, delta=f"{negativas/len(df_filtered)*100:.1f}%", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    neutras = len(df_filtered[df_filtered['sentiment'] == 'neutro'])
    st.metric("Notícias Neutras", neutras, delta=f"{neutras/len(df_filtered)*100:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

# Layout com abas
tab1, tab2, tab3, tab4 = st.tabs(["📈 Gráficos", "☁️ Nuvem de Palavras", "📰 Notícias", "📊 Análise Temporal"])

with tab1:
    # Gráfico de Pizza
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição de Sentimentos")
        fig_pizza = px.pie(
            df_filtered, 
            names='sentiment', 
            title='Proporção de Sentimentos',
            color='sentiment',
            color_discrete_map={'positivo': '#2ecc71', 'negativo': '#e74c3c', 'neutro': '#f39c12'}
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with col2:
        st.subheader("📅 Distribuição por Data")
        if 'data' in df_filtered.columns:
            time_series = df_filtered.groupby(['data', 'sentiment']).size().reset_index(name='count')
            fig_time = px.bar(
                time_series, 
                x='data', 
                y='count',
                color='sentiment',
                title='Notícias por Data',
                color_discrete_map={'positivo': '#2ecc71', 'negativo': '#e74c3c', 'neutro': '#f39c12'}
            )
            st.plotly_chart(fig_time, use_container_width=True)
        else:
            st.info("Dados temporais não disponíveis")

with tab2:
    # Nuvem de Palavras
    st.subheader("☁️ Nuvem de Palavras")
    
    text_source = st.radio(
        "Fonte do texto:",
        ["Títulos", "Descrições", "Ambos"],
        horizontal=True
    )
    
    if text_source == "Títulos":
        all_text = ' '.join(df_filtered['title'].dropna().astype(str))
    elif text_source == "Descrições":
        all_text = ' '.join(df_filtered['description'].dropna().astype(str))
    else:
        all_text = ' '.join(df_filtered['title'].dropna().astype(str) + ' ' + df_filtered['description'].dropna().astype(str))
    
    if all_text.strip():
        wordcloud = WordCloud(
            width=800, 
            height=400, 
            background_color='white',
            colormap='viridis'
        ).generate(all_text)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Palavras mais Frequentes', fontsize=16)
        st.pyplot(fig)
    else:
        st.warning("Não há texto suficiente para gerar nuvem de palavras.")

with tab3:
    # Tabela de Notícias
    st.subheader("📰 Lista de Notícias")
    
    for _, row in df_filtered.iterrows():
        # Determinar cor baseada no sentimento
        if row['sentiment'] == 'positivo':
            border_color = '#2ecc71'
        elif row['sentiment'] == 'negativo':
            border_color = '#e74c3c'
        else:
            border_color = '#f39c12'
        
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; padding: 10px; margin: 10px 0;'>
            <h4 style='margin: 0;'>{row['title']}</h4>
            <p style='margin: 5px 0; color: #666;'>{row['description']}</p>
            <strong>Sentimento:</strong> <span style='color: {border_color};'>{row['sentiment']}</span>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    # Análise temporal avançada
    st.subheader("📈 Análise Temporal Detalhada")
    
    if 'data' in df_filtered.columns:
        # Gráfico de linha temporal
        time_analysis = df_filtered.groupby([pd.Grouper(key='data', freq='W'), 'sentiment']).size().unstack(fill_value=0)
        
        fig = go.Figure()
        for sentiment in time_analysis.columns:
            fig.add_trace(go.Scatter(
                x=time_analysis.index,
                y=time_analysis[sentiment],
                name=sentiment,
                mode='lines+markers',
                line=dict(width=3)
            ))
        
        fig.update_layout(
            title='Evolução Temporal dos Sentimentos',
            xaxis_title='Data',
            yaxis_title='Número de Notícias',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas temporais
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Período Total", f"{(df_filtered['data'].max() - df_filtered['data'].min()).days} dias")
        with col2:
            st.metric("Média Semanal", f"{len(df_filtered) / ((df_filtered['data'].max() - df_filtered['data'].min()).days / 7):.1f} notícias/semana")
    else:
        st.info("Dados temporais não disponíveis para análise")

# Rodapé com aviso de limitações
st.markdown("---")
st.warning("""
**⚠️ Limitações do Modelo:** 
Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos. 
Os resultados devem ser interpretados com cautela.
""")

# Informações técnicas
with st.expander("ℹ️ Informações Técnicas"):
    st.write(f"**Total de dados:** {len(df)} notícias")
    st.write(f"**Período:** {df['data'].min().strftime('%d/%m/%Y') if 'data' in df.columns else 'N/A'} a {df['data'].max().strftime('%d/%m/%Y') if 'data' in df.columns else 'N/A'}")
    st.write(f"**Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")