# extract_mdl_course.py
import mysql.connector
import json
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='nmit@123',
    database='moodle',
    unix_socket='/var/run/mysqld/mysqld.sock'
)
cursor = conn.cursor(dictionary=True)

# Query relevant columns
cursor.execute("""
    SELECT id, fullname, shortname, summary, startdate
    FROM mdl_course
""")
rows = cursor.fetchall()

# Convert each row to a natural-language text
course_data = []
for row in rows:
    start_date_str = datetime.fromtimestamp(row['startdate']).strftime('%Y-%m-%d') if row['startdate'] else "Unknown start date"
    course_text = f"{row['fullname']} ({row['shortname']}) starts on {start_date_str}. {row['summary'] or ''}"
    course_data.append({
        "id": row['id'],
        "text": course_text.strip()
    })

# Save to JSON
with open("mdl_course_text.json", "w") as f:
    json.dump(course_data, f, indent=2)

print(f"[✓] Extracted and saved {len(course_data)} course records to mdl_course_text.json")

# Close DB
cursor.close()
conn.close()
