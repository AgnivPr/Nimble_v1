import mysql.connector
import pandas as pd

# Step 1: Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nmit@123",
    database="moodle"
)

# Step 2: Fetch selected columns from mdl_user
query = """
SELECT id, firstname, lastname, email, city, country, department, institution, description
FROM mdl_user
WHERE deleted = 0 AND suspended = 0
"""
df = pd.read_sql(query, conn)

# Step 3: Convert each row into text format
def row_to_text(row):
    return (
        f"User ID: {row['id']}\n"
        f"Name: {row['firstname']} {row['lastname']}\n"
        f"Email: {row['email']}\n"
        f"City: {row['city'] or 'N/A'}\n"
        f"Country: {row['country'] or 'N/A'}\n"
        f"Department: {row['department'] or 'N/A'}\n"
        f"Institution: {row['institution'] or 'N/A'}\n"
        f"Description: {row['description'] or 'N/A'}"
    )

# Apply the formatting
df['text'] = df.apply(row_to_text, axis=1)

# Step 4: Save to a JSON file (for embedding later)
df[['id', 'text']].to_json('mdl_user_text.json', orient='records', indent=2)

print(f"[✓] Extracted and saved {len(df)} user records to mdl_user_text.json")
