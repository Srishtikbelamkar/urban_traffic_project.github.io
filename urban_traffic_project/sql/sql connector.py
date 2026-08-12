import mysql.connector

# ---------------------------------------
# Connect Python to MySQL
# ---------------------------------------

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="urban_traffic_db"
)

cursor = connection.cursor()

# 1. Display total number of records
# =======================================

query = """
SELECT COUNT(*) AS Total_Records
FROM  accident_data;
"""

cursor.execute(query)

result = cursor.fetchone()

print("\nTotal Records:", result[0])

# 2. Average Traffic Volume
# =======================================

query = """
SELECT AVG(Traffic_Volume) AS Average_Traffic
FROM accident_data;
"""

cursor.execute(query)

result = cursor.fetchone()

print("\nAverage Traffic Volume:", round(result[0], 2))


print("Connected to MySQL successfully!")

