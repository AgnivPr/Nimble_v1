import pymysql
import pandas as pd

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",  # Change if needed
    password="nmit@123",  # Change to your actual password
    database="test_db"  # Change to your actual database name
)

# Fetch data from a table (modify table/column names as needed)
query = "SELECT id, name, course, notes FROM students;"
df = pd.read_sql(query, conn)

# Close the database connection
conn.close()

# Combine multiple text columns into one (modify as needed)
df["combined_text"] = df[["name", "course", "notes"]].astype(str).agg(" ".join, axis=1)
# Convert DataFrame to a list of text records
texts = df["combined_text"].tolist()
print("Extracted Data:", texts)  # Debugging purpose

# Save extracted data for later steps
df.to_csv("extracted_data.csv", index=False)

print("Data extraction completed. Saved as extracted_data.csv.")

