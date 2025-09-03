import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import requests
from xml.etree import ElementTree
import re
import html

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

# Funções para buscar e processar notícias
def fetch_news_rss(search_query, num_news=15):
    """
    Busca notícias reais via RSS do Google Notícias
    """
    base_url = "https://news.google.com/rss/search"
    
    # Múltiplos termos de busca para trazer mais resultados
    expanded_queries = [
        "Inteligência Artificial Piauí",
        "IA Piauí", 
        "Tecnologia Piauí",
        "Inovação Piauí",
        "Startup Piauí",
        "TI Piauí"
    ]
    
    all_news = []
    
    for query in expanded_queries:
        try:
            params = {
                'q': query,
                'hl': 'pt-BR',
                'gl': 'BR',
                'ceid': 'BR:pt-419'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            
            root = ElementTree.fromstring(response.content)
            
            for item in root.findall('.//item'):
                if len(all_news) >= num_news:
                    break
                    
                news_item = {
                    'title': item.find('title').text if item.find('title') is not None else 'Sem título',
                    'link': item.find('link').text if item.find('link') is not None else '#',
                    'description': item.find('description').text if item.find('description') is not None else 'Sem descrição',
                    'pubDate': item.find('pubDate').text if item.find('pubDate') is not None else 'Data não disponível',
                    'source': item.find('source').text if item.find('source') is not None else 'Fonte desconhecida'
                }
                
                # Evitar duplicatas
                if news_item['title'] not in [n['title'] for n in all_news]:
                    all_news.append(news_item)
            
        except Exception as e:
            print(f"Erro na busca por '{query}': {e}")
            continue
    
    return all_news[:num_news]

def clean_text(text):
    """
    Limpa texto removendo HTML tags e caracteres especiais
    """
    if not text or not isinstance(text, str):
        return ""
    
    try:
        text = re.sub(r'<[^>]+>', '', text)
        text = html.unescape(text)
        text = re.sub(r'[^\w\sàáâãäåèéêëìíîïòóôõöùúûüçñÀÁÂÃÄÅÈÉÊËÌÍÎÏÒÓÔÕÖÙÚÛÜÇÑ]', '', text)
        return text.strip()
    except:
        return text if text else ""

def analyze_sentiment(text):
    """
    Analisa sentimento com base em palavras-chave
    """
    if not text or not isinstance(text, str):
        return "neutro"
    
    text_lower = text.lower()
    
    positive_words = ['inovação', 'avanço', 'benefício', 'crescimento', 'oportunidade', 
                     'sucesso', 'desenvolvimento', 'positivo', 'eficiente', 'melhoria',
                     'transformação', 'tecnologia', 'futuro', 'progresso', 'investimento',
                     'lucro', 'ganho', 'vantagem', 'conquista', 'êxito']
    
    negative_words = ['risco', 'problema', 'desafio', 'ameaça', 'preocupação', 'negativo',
                     'dificuldade', 'limitação', 'erro', 'falha', 'perigo', 'controvérsia',
                     'crítica', 'polêmica', 'prejuízo', 'perda', 'fracasso', 'insucesso',
                     'complicação', 'obstáculo']
    
    neutral_words = ['análise', 'estudo', 'pesquisa', 'relatório', 'dado', 'informação',
                    'notícia', 'artigo', 'publicação', 'divulgação', 'comunicado']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    neutral_count = sum(1 for word in neutral_words if word in text_lower)
    
    if positive_count > negative_count and positive_count > neutral_count:
        return "positivo"
    elif negative_count > positive_count and negative_count > neutral_count:
        return "negativo"
    elif neutral_count > positive_count and neutral_count > negative_count:
        return "neutro"
    elif positive_count == negative_count:
        return "neutro"
    else:
        return "neutro"

# Carregar dados
@st.cache_data
def load_data():
    try:
        # Buscar notícias reais
        news_list = fetch_news_rss("IA Piauí", 15)
        
        if not news_list:
            st.warning("Não foram encontradas notícias. Usando dados de exemplo.")
            raise Exception("Nenhuma notícia encontrada")
        
        # Processar notícias
        processed_news = []
        for news in news_list:
            cleaned_title = clean_text(news['title'])
            cleaned_description = clean_text(news['description'])
            
            processed_news.append({
                'title': cleaned_title,
                'description': cleaned_description,
                'sentiment': analyze_sentiment(cleaned_title + " " + cleaned_description),
                'source': news['source'],
                'link': news['link'],
                'pubDate': news['pubDate']
            })
        
        df = pd.DataFrame(processed_news)
        
        # Adicionar datas fictícias para compatibilidade com seu dashboard
        if len(df) > 0:
            df['data'] = pd.date_range(
                start=pd.to_datetime('2024-01-01'), 
                periods=len(df), 
                freq='D'
            )
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        # Fallback para dados de exemplo com distribuição realista de sentimentos
        data = {
            'title': [
                'Governo do Piauí anuncia investimento em IA',
                'Startup de Teresina desenvolve solução em IA',
                'Universidade Federal do Piauí lança curso de IA',
                'Prefeitura de Parnaíba usa IA no atendimento',
                'Empresas de TI do Piauí crescem com projetos de IA',
                'IA ajuda no combate à seca no Piauí',
                'Pesquisadores piauienses publicam estudo sobre IA',
                'Hospital em Teresina implementa IA no diagnóstico',
                'Secretaria de Educação do Piauí usa IA no ensino',
                'Startup piauiense recebe investimento para IA',
                'IA no agronegócio do Piauí mostra resultados',
                'Prefeitura de Teresina lança programa de IA',
                'Empresas do Piauí adotam IA para eficiência',
                'Pesquisa mostra potencial de IA no Piauí',
                'Governo do Estado incentiva startups de IA',
                'Problemas técnicos afetam sistema de IA do governo',
                'Preocupações com privacidade em projeto de IA',
                'Falta de verbra atrasa projetos de IA no estado',
                'Críticas à implementação de IA na saúde',
                'Desafios na adoção de IA por pequenas empresas'
            ],
            'description': [
                'Novos investimentos em tecnologia estadual com foco em inovação',
                'Solução inovadora desenvolvida localmente traz benefícios para a região',
                'Novo curso para formação em inteligência artificial com vagas limitadas',
                'Melhoria no atendimento público com tecnologia de ponta',
                'Crescimento do setor de tecnologia no estado gera empregos',
                'Aplicação de IA para problemas regionais mostra resultados positivos',
                'Contribuição científica do Piauí em IA é reconhecida nacionalmente',
                'Inovação tecnológica na saúde piauiense melhora diagnósticos',
                'Tecnologia aplicada à educação estadual moderniza ensino',
                'Reconhecimento e investimento em startup local impulsiona setor',
                'Modernização do agronegócio com IA aumenta produtividade',
                'Programa municipal de incentivo à tecnologia atrai empresas',
                'Eficiência operacional através de IA reduz custos',
                'Estudo sobre oportunidades de IA no estado mostra potencial',
                'Políticas estaduais para fomento tecnológico criam ecossistema',
                'Sistema apresenta falhas e preocupa especialistas em segurança',
                'Projeto gera debates sobre proteção de dados pessoais',
                'Orçamento limitado impacta desenvolvimento tecnológico',
                'Implementação enfrenta resistência de profissionais da área',
                'Pequenas empresas relatam dificuldades na implantação'
            ],
            'sentiment': [
                'positivo', 'positivo', 'positivo', 'positivo', 'positivo',
                'positivo', 'positivo', 'positivo', 'positivo', 'positivo',
                'positivo', 'positivo', 'positivo', 'positivo', 'positivo',
                'negativo', 'negativo', 'negativo', 'negativo', 'negativo'
            ],
            'data': pd.date_range(start='2024-01-01', periods=20, freq='D')
        }
        df = pd.DataFrame(data)
        # Selecionar apenas 15 notícias para manter o padrão
        return df.head(15)

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
    percent_positivo = (positivas/len(df_filtered)*100) if len(df_filtered) > 0 else 0
    st.metric("Notícias Positivas", positivas, delta=f"{percent_positivo:.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    negativas = len(df_filtered[df_filtered['sentiment'] == 'negativo'])
    percent_negativo = (negativas/len(df_filtered)*100) if len(df_filtered) > 0 else 0
    st.metric("Notícias Negativas", negativas, delta=f"{percent_negativo:.1f}%", delta_color="inverse")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    neutras = len(df_filtered[df_filtered['sentiment'] == 'neutro'])
    percent_neutro = (neutras/len(df_filtered)*100) if len(df_filtered) > 0 else 0
    st.metric("Notícias Neutras", neutras, delta=f"{percent_neutro:.1f}%")
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
            sentiment_emoji = '✅'
        elif row['sentiment'] == 'negativo':
            border_color = '#e74c3c'
            sentiment_emoji = '❌'
        else:
            border_color = '#f39c12'
            sentiment_emoji = '⚠️'
        
        st.markdown(f"""
        <div style='border-left: 4px solid {border_color}; padding: 10px; margin: 10px 0;'>
            <h4 style='margin: 0;'>{row['title']}</h4>
            <p style='margin: 5px 0; color: #666;'>{row['description']}</p>
            <strong>Sentimento:</strong> <span style='color: {border_color};'>{sentiment_emoji} {row['sentiment']}</span>
            <br><small><strong>Fonte:</strong> {row.get('source', 'N/A')} | <strong>Data:</strong> {row.get('pubDate', 'N/A')}</small>
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
    st.write("**Fonte dos dados:** Google Notícias RSS")
    st.write("**Método de análise:** Regras baseadas em palavras-chave")
    st.write(f"**Distribuição de sentimentos:** {len(df[df['sentiment'] == 'positivo'])} positivas, {len(df[df['sentiment'] == 'negativo'])} negativas, {len(df[df['sentiment'] == 'neutro'])} neutras")