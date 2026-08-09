import duckdb
import io
import pandas as pd

con = duckdb.connect(database="database/exercises_sql_tables.duckdb", read_only=False)

dataf = {
    "theme": ["cross joins", "window functions"],
    "exercises": ["food_and_beverages", "simple_window"],
    "tables": [["beverages", "food_items"], "simple_window"],
    "last_reviewed": ["1970-01-01", "1970-01-01"],
}

memory_state_df = pd.DataFrame(dataf)
con.execute("CREATE TABLE IF NOT EXISTS memory_state AS SELECT * FROM memory_state_df")

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

con.execute("CREATE TABLE IF NOT EXISTS beverages AS SELECT * FROM beverages")
con.execute("CREATE TABLE IF NOT EXISTS food_items AS SELECT * FROM food_items")
