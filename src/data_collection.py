import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
import time

def fetch_google_news_rss(query="Inteligência Artificial Piauí"):
    """
    Coleta notícias do Google News RSS baseado na query
    """
    try:
        # Formata a query para URL
        formatted_query = query.replace(" ", "+")
        url = f"https://news.google.com/rss/search?q={formatted_query}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
        
        # Headers para simular navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Faz a requisição
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        return response.text
        
    except Exception as e:
        print(f"Erro ao buscar notícias: {e}")
        return None

def parse_rss_to_dataframe(xml_content):
    """
    Converte o XML do RSS para DataFrame
    """
    try:
        # Parse do XML
        root = ET.fromstring(xml_content)
        
        news_data = []
        
        # Namespace do RSS
        ns = {'': 'http://purl.org/rss/1.0/', 
              'media': 'http://search.yahoo.com/mrss/'}
        
        # Extrai cada item de notícia
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            
            news_data.append({
                'title': title,
                'link': link,
                'pub_date': pub_date,
                'description': description,
                'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return pd.DataFrame(news_data)
        
    except Exception as e:
        print(f"Erro ao parsear XML: {e}")
        return pd.DataFrame()

def collect_news():
    """
    Função principal para coletar notícias
    """
    print("🔍 Coletando notícias sobre IA no Piauí...")
    
    # Queries de busca
    queries = [
        "Inteligência Artificial Piauí",
        "IA Piauí", 
        "SIA Piauí",
        "Tecnologia Piauí",
        "Inovação Piauí"
    ]
    
    all_news = pd.DataFrame()
    
    for query in queries:
        print(f"Buscando: {query}")
        
        # Coleta do RSS
        xml_content = fetch_google_news_rss(query)
        
        if xml_content:
            # Converte para DataFrame
            df_news = parse_rss_to_dataframe(xml_content)
            
            if not df_news.empty:
                df_news['search_query'] = query
                all_news = pd.concat([all_news, df_news], ignore_index=True)
        
        # Delay para não sobrecarregar
        time.sleep(2)
    
    # Remove duplicatas
    if not all_news.empty:
        all_news = all_news.drop_duplicates(subset=['title', 'link'])
        print(f"✅ Coletadas {len(all_news)} notícias únicas")
        
        # Salva os dados brutos
        all_news.to_csv('data/raw_news.csv', index=False, encoding='utf-8')
        print("💾 Dados salvos em data/raw_news.csv")
        
    return all_news

if __name__ == "__main__":
    # Executa a coleta
    news_df = collect_news()
    
    if news_df.empty:
        print("❌ Nenhuma notícia encontrada. Usando dados de exemplo.")
        # Cria dados de exemplo se não encontrar nada
        example_data = {
            'title': ['Governo do Piauí investe em IA', 'Startup de IA no Piauí cresce'],
            'description': ['Novo investimento em tecnologia', 'Empresa local recebe funding'],
            'pub_date': [datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d')],
            'link': ['#', '#'],
            'collected_at': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * 2
        }
        pd.DataFrame(example_data).to_csv('data/raw_news.csv', index=False, encoding='utf-8')