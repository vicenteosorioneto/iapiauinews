import pandas as pd
import re
from bs4 import BeautifulSoup

def clean_text(text):
    """
    Limpa o texto removendo tags HTML, caracteres especiais e espaços extras.
    """
    if pd.isna(text):
        return ""

    # Remove tags HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Remove caracteres especiais
    text = re.sub(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕçÇ\s]', '', text)

    # Remove espaços extras
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def analyze_sentiment(text, positive_words, negative_words):
    """
    Classifica o sentimento com base em listas de palavras.
    """
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)

    if positive_count > negative_count:
        return "positivo"
    elif negative_count > positive_count:
        return "negativo"
    else:
        return "neutro"

# Definindo minha listas de palavras
positive_words = ["avanço", "inovação", "benefício", "crescimento", "oportunidade", "desenvolvimento", "tecnologia", "educação", "investimento", "futuro"]
negative_words = ["risco", "ameaça", "desemprego", "problema", "preocupação", "perigo", "vício", "viés", "invasão", "culpa"]
def main():
    # meu código principal aqui
   def main():
    # 1. Carregar os dados coletados (supondo que estejam em um CSV)
    df = pd.read_csv('../data/raw_news.csv')

    # 2. Limpar os textos (título e descrição)
    df['cleaned_title'] = df['title'].apply(clean_text)
    df['cleaned_description'] = df['description'].apply(clean_text)

    # 3. Combinar título e descrição para análise
    df['combined_text'] = df['cleaned_title'] + " " + df['cleaned_description']

    # 4. Classificar o sentimento
    df['sentiment'] = df['combined_text'].apply(
        lambda text: analyze_sentiment(text, positive_words, negative_words)
    )

    # 5. Salvar os dados processados
    df.to_csv('../data/processed_news.csv', index=False)
    print("Processamento concluído! Dados salvos em '../data/processed_news.csv'")

    return df

if __name__ == "__main__":
    main()