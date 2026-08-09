import io
import string

import duckdb
import pandas as pd
import streamlit as st
import ast

st.write("""
# SQL revision
Spaced repetition system SQL
""")

con = duckdb.connect(database="database/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to revise ?",
        ["cross joins", "group by", "window functions"],
        index=None,
        placeholder="Select a theme ...",
    )
    st.write("you selected", theme)
    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercises"]
    with open(f"answer/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()


query = st.text_area("Entrez votre requête SQL :", key="user_input")


if query:
    result = con.execute(query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_differences = abs(result.shape[0] - solution_df.shape[0])
    if n_lines_differences != 0:
        st.write(
            f"Your result has {n_lines_differences} lines differences with the solution"
        )
tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)


with tab3:
    st.write(answer)
