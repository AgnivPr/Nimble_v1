# extract_forum_posts.py

import json
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nmit@123",
    database="moodle"
)
cursor = conn.cursor(dictionary=True)

# Extract subject and message
cursor.execute("SELECT id, subject, message FROM mdl_forum_posts")
rows = cursor.fetchall()

# Format for semantic use
formatted = []
for row in rows:
    text = f"Subject: {row['subject']}\nMessage: {row['message']}"
    formatted.append({"id": row["id"], "text": text})

# Save to JSON
with open("mdl_forum_posts_text.json", "w") as f:
    json.dump(formatted, f, indent=2)

print(f"[✓] Extracted {len(formatted)} forum posts into mdl_forum_posts_text.json")
