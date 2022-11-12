import sqlite3
conn = sqlite3.connect("application.db")
data = conn.execute("select company_id,password_comp from Company;")
for row in data:
  print(row)
conn.close()