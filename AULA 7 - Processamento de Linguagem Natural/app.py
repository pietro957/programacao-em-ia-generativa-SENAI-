from deep_translator import GoogleTranslator
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import sqlite3
import streamlit as st
import timeit

conn = sqlite3.connect("dados.db")  # criando o banco
cursor = conn.cursor()  # cursor

cursor.execute("""CREATE TABLE IF NOT EXISTS dados(
               
                id INTEGER,
                sentimento TEXT,
                texto TEXT
               
               )
""")

conn.commit()

nltk.download("vader_lexicon")
nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab")

id_ = st.number_input("Numero ID: ", value=0)
text = st.text_input("em Portugues: ")

tokens = nltk.word_tokenize(text, language="portuguese")
print(tokens)

# stop words
st_ = set(stopwords.words("portuguese"))
palavras_filtradas = [palavra for palavra in tokens if palavra not in st_]

print(palavras_filtradas)

# classificação
sia = SentimentIntensityAnalyzer()

sentimento_ = sia.polarity_scores(text)
sentimento = sentimento_["compound"]

print(sentimento)

# CORREÇÃO: Exibimos o header separadamente e mantemos 'sentimento' (ou sua conversão) em 'numero'
st.header(sentimento)
numero = float(sentimento)  # Convertendo para string ou mantendo o float original

if sentimento >= 0.5:
  st.write("Usuario feliz")

elif sentimento <= -0.1:
  st.write("Triste e insastisfeito")

elif sentimento == 0:
  st.write("neutro")

# Inserção no banco apenas se houver texto digitado para evitar registros vazios ao carregar a página
if text:
  cursor.execute(
      "INSERT INTO dados (id, sentimento, texto) VALUES (?, ?, ?)",
      (id_, numero, text),
  )
  conn.commit()

# CORREÇÃO: Buscamos os dados DEPOIS do INSERT para que o novo registro apareça na tabela
df = pd.read_sql_query("SELECT * FROM dados", conn)

# Fechamos a conexão após realizar todas as operações
conn.close()

st.dataframe(df) 

