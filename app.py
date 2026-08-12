import io
import string
import os
import duckdb
import pandas as pd
import streamlit as st
from datetime import date, timedelta, datetime

st.write("""
# SQL revision
Spaced repetition system SQL
""")

if "database" not in os.listdir():
    os.mkdir("database")
if "exercises_sql_tables.duckdb" not in os.listdir("database"):
    exec(open("init_database.py").read())

def comparison_answer_solution(query):
    global result, e
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

con = duckdb.connect(database="database/exercises_sql_tables.duckdb", read_only=False)

with st.sidebar:
    available_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state")
    theme = st.selectbox(
        "What would you like to revise ?",
        available_theme_df,
        index=None,
        placeholder="Select a theme ...",
    )

    if theme :
        st.write(f"you selected {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"
    else :
        select_exercise_query = f"SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercise_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercises"]
    with open(f"answer/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()


query = st.text_area("Entrez votre requête SQL :", key="user_input")




if query:
    comparison_answer_solution(query)

for n_days in [2, 7, 20]:
    if st.button(f'Revoir dans {n_days} jours'):
        next_review = date.today() + timedelta(n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercises = '{exercise_name}'")
        st.rerun()
if st.button('Reset'):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"Table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)


with tab3:
    st.write(answer)
