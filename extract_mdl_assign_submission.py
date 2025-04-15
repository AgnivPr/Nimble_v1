import mysql.connector
import json
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="nmit@123",  # Replace with your actual password
    database="moodle",
    unix_socket="/var/run/mysqld/mysqld.sock"
)

cursor = conn.cursor(dictionary=True)

# Fetch relevant fields
query = """
SELECT id, assignment, userid, timecreated, timemodified, status, attemptnumber, latest
FROM mdl_assign_submission
"""
cursor.execute(query)
rows = cursor.fetchall()

# Convert to readable format
data = []
for row in rows:
    created = datetime.fromtimestamp(row["timecreated"]).strftime("%Y-%m-%d %H:%M:%S") if row["timecreated"] else "N/A"
    modified = datetime.fromtimestamp(row["timemodified"]).strftime("%Y-%m-%d %H:%M:%S") if row["timemodified"] else "N/A"
    text = (
        f"User ID {row['userid']} submitted assignment ID {row['assignment']}. "
        f"Status: {row['status']}. Attempt: {row['attemptnumber']}. "
        f"Submitted at {created}. Modified at {modified}. Latest: {row['latest']}"
    )
    data.append({"id": row["id"], "text": text})

# Save to JSON
with open("mdl_assign_submission_text.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"[✓] Extracted and saved {len(data)} assignment submissions to mdl_assign_submission_text.json")

cursor.close()
conn.close()
