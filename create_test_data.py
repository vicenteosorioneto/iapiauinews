import pandas as pd

data = {
    'title': ['IA avança no Piauí', 'Preocupações com IA'],
    'description': ['Grande inovação tecnológica.', 'Riscos do desemprego.']
}

df = pd.DataFrame(data)
df.to_csv('data/raw_news.csv', index=False)
print("✅ Arquivo raw_news.csv criado com sucesso!")