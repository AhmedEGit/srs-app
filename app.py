

import io
import string

import duckdb
import pandas as pd
import streamlit as st

st.write("""
# SQL revision
Spaced repetition system SQL
""")

csv1 = """
beverage, price
juice, 2.5
tea, 2
coffee, 1.5
"""

csv2 = """
food_item, food_price
croissant juice, 3.5
chocolatine, 1.5
cookie, 1.5
"""

beverages = pd.read_csv(io.StringIO(csv1))
food_items = pd.read_csv(io.StringIO(csv2))


with st.sidebar:
    option = st.selectbox(
        "What would you like to revise ?", ["joins", "group by", "window functions"]
    )
    st.write("you selected", option)


query = st.text_area("Entrez votre requête SQL :", key="user_input")

answer = "SELECT * FROM beverages CROSS JOIN food_items"
solution = duckdb.query(answer).df()

if query:
    result = duckdb.query(query).df()
    st.dataframe(result)
    try:
        result = result[solution.columns]
        st.dataframe(result.compare(solution))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_differences = abs(result.shape[0] - solution.shape[0])
    if n_lines_differences != 0:
        st.write(
            f"Your result has {n_lines_differences} lines differences with the solution"
        )
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    st.write("Table : beverages")
    st.dataframe(beverages)
    st.write("Table: food_items")
    st.dataframe(food_items)
    st.write("expected :")
    st.dataframe(solution)

with tab3:
    st.write(answer)
