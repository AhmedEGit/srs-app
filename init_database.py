import duckdb
import io
import pandas as pd

con = duckdb.connect(database="database/exercises_sql_tables.duckdb", read_only=False)

dataf = {
    "theme": ["cross joins", "cross joins"],
    "exercises": ["food_and_beverages", "sizes_and_trademarks"],
    "tables": [["beverages", "food_items"], ["sizes", "trademarks"]],
    "last_reviewed": ["1980-01-01", "1970-01-01"],
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

size = """
size
xs
M
L
XL
"""
sizes = pd.read_csv(io.StringIO(size))

trademark = """
trademark
Nike
asphalte
adidas
Lewis
"""
trademarks = pd.read_csv(io.StringIO(trademark))

con.execute("CREATE TABLE IF NOT EXISTS sizes AS SELECT * FROM sizes")
con.execute("CREATE TABLE IF NOT EXISTS trademarks AS SELECT * FROM trademarks")

con.close()
