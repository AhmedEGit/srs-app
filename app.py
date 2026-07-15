import streamlit as st
import pandas as pd
import duckdb
import io

st.write("""
# SQL revision
Spaced repetition system SQL
""")


csv1 = """
food_item, food_price
chocolatine, 2
cookie, 3
pain, 1
"""
csv2 = """
food_item, beverages
chocolatine, jus
cookie, café
"""

food = pd.read_csv(io.StringIO(csv1))
beverages = pd.read_csv(io.StringIO(csv2))

answer = "SELECT * FROM food CROSS JOIN beverages"
solution = duckdb.sql(answer).df()

with st.sidebar:
    option = st.selectbox("What would you like to revise ?", ["joins", "group by","window functions"])
    st.write("you choose", option)

dataf = pd.DataFrame({"a": [1, 2, 3], "b": [9, 8, 7]})
st.dataframe(dataf)

user_input = st.text_area("Entrez votre requête SQL :")

if user_input.strip():
    try:
        user_query = duckdb.query(user_input).df()
        st.write("Voici le résultat :")
        st.dataframe(user_query)
    except Exception as e:
        st.error(f"Erreur SQL : {e}")


