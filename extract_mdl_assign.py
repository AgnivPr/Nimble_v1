# extract_mdl_assign.py

import json
import pymysql
import pandas as pd
from datetime import datetime

# Connect to MySQL
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='nmit@123',  # your password here if any
    database='moodle',
    cursorclass=pymysql.cursors.DictCursor
)

# Query to join mdl_assign with mdl_course to get course names
query = """
SELECT 
    a.id AS assignment_id,
    c.fullname AS course_name,
    a.name AS assignment_name,
    a.intro AS description,
    FROM_UNIXTIME(a.duedate) AS due_date,
    a.grade AS max_grade
FROM mdl_assign a
JOIN mdl_course c ON a.course = c.id
"""

# Load into DataFrame
df = pd.read_sql(query, conn)

# Format each row as a readable string for embeddings
def format_assignment(row):
    return {
        "assignment_id": row["assignment_id"],
        "text": f"""Assignment: {row['assignment_name']}
Course: {row['course_name']}
Description: {row['description']}
Due Date: {row['due_date']}
Max Grade: {row['max_grade']}"""
    }

formatted_data = [format_assignment(row) for _, row in df.iterrows()]

# Save to JSON
with open("mdl_assign_text.json", "w") as f:
    json.dump(formatted_data, f, indent=2)

print(f"[✓] Extracted and saved {len(formatted_data)} assignment records to mdl_assign_text.json")
