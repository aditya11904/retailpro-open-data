import sqlite3
import pandas as pd
import json

# Read SQL from file
with open("q-sql-correlation-github-pages.sql", "r") as f:
    sql_script = f.read()

# Create SQLite DB in memory
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.executescript(sql_script)
conn.commit()

# Load data into pandas
df = pd.read_sql_query("SELECT Footfall, Avg_Basket, Returns FROM retail_data", conn)

# Calculate correlations
correlations = {
    "Footfall-Avg_Basket": df["Footfall"].corr(df["Avg_Basket"]),
    "Footfall-Returns": df["Footfall"].corr(df["Returns"]),
    "Avg_Basket-Returns": df["Avg_Basket"].corr(df["Returns"])
}

# Find the strongest correlation
strongest_pair = max(correlations, key=lambda k: abs(correlations[k]))
result = {
    "pair": strongest_pair,
    "correlation": round(correlations[strongest_pair], 4)
}

# Print result as JSON
print(json.dumps(result, indent=2))
