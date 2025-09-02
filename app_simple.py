import streamlit as st
import pandas as pd

st.title("🤖 Dashboard IA Piauí - SIMPLES")
df = pd.read_csv("data/processed_news.csv")
st.write(f"Total de notícias: {len(df)}")
st.dataframe(df)
st.success("Funcionando!")
