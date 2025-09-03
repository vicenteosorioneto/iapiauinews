
#  Decisões Técnicas

##  Por que análise baseada em regras e não Machine Learning?

**Decisão:** Utilizar abordagem baseada em regras com listas de palavras positivas/negativas.

**Motivos:**
-  **Simplicidade:** Mais fácil de implementar e explicar
-  **Transparência:** As regras são explícitas e compreensíveis
-  **Recursos:** Não requer dados de treinamento ou modelo complexo
-  **Velocidade:** Mais rápido para um MVP (Minimum Viable Product)

**Limitações aceitas:**
-  Não captura sarcasmo ou ironia
-  Pode errar em contextos complexos
-  Depende da qualidade das listas de palavras

##  Escolha de Tecnologias

**Streamlit:** Escolhido por ser a forma mais rápida de criar dashboards interativos em Python sem necessidade de front-end complexo.

**Pandas:** Para manipulação eficiente dos dados tabulares.

**Plotly:** Para gráficos interativos e modernos.

##  Decisões de Design

**Dashboard simples:** Focado na clareza das informações rather than elementos visuais complexos.

**Avisos de limitação:** Inclusão destacada das limitações do modelo para transparência.

##  Fluxo de Dados

1. Coleta → 2. Limpeza → 3. Análise de Sentimento → 4. Visualização

**Arquitetura simples** propositalmente para facilitar manutenção e entendimento.