# 🤖 IA Piauí Monitor - Dashboard de Análise de Notícias

Dashboard interativo para monitoramento e análise de sentimentos sobre Inteligência Artificial no estado do Piauí.

## 📊 Sobre o Projeto

Este projeto foi desenvolvido como parte de um case técnico para monitoramento da percepção pública sobre Inteligência Artificial no Piauí. O sistema coleta, processa e analisa notícias em tempo real, classificando o sentimento das publicações e apresentando os resultados através de visualizações interativas.

### 🎯 Objetivos
- Monitorar menções sobre IA no Piauí em fontes de notícias
- Realizar análise de sentimento automatizada
- Identificar temas recorrentes e tendências
- Fornecer insights através de visualizações intuitivas

### 👥 Público-Alvo
- Estudantes de graduação em Tecnologia e áreas afins
- Pesquisadores e acadêmicos
- Gestores públicos e tomadores de decisão
- Empresas de tecnologia locais
- Comunidade interessada em IA no Piauí

## 🚀 Status do Projeto

**✅ Funcional - Versão 1.0**

O projeto está totalmente funcional com as seguintes características:
- ✅ Coleta automática de notícias via RSS
- ✅ Análise de sentimento baseada em regras
- ✅ Dashboard interativo com Streamlit
- ✅ Visualizações gráficas (Plotly e Matplotlib)
- ✅ Filtros avançados por sentimento e data
- ✅ Nuvem de palavras dinâmica

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit** - Dashboard interativo
- **Pandas** - Manipulação de dados
- **Plotly** - Visualizações gráficas
- **Matplotlib** - Nuvem de palavras
- **Requests** - Requisições HTTP
- **BeautifulSoup** - Processamento de HTML/XML

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. Clone o repositório
git clone https://github.com/vicenteosorioneto/iapiauinews.git

2. Entre na pasta do projeto
cd iapiauinews

3. Instale as dependências
pip install -r requirements.txt

4. Execute o dashboard Streamlit
streamlit run app.py
