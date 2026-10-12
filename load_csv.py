import csv
import sqlite3



def load_csv_to_db(csv_path, db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS tables_info (name TEXT, rows_count INTEGER, owner TEXT)")
    cur.execute("DELETE FROM tables_info")

    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO tables_info VALUES (?, ?, ?)",
                (row["name"], int(row["rows"]), row["owner"])
            )

    conn.commit()
    conn.close()

def report_by_owner(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT owner, COUNT(*) AS cnt_tables, SUM(rows_count) AS cnt_rows
        FROM tables_info
        GROUP BY owner
    """)
    for row in cur.fetchall():
        print(f"{row['owner']}: {row['cnt_tables']} tables, {row['cnt_rows']} rows")

    conn.close()


CSV_PATH = r"table_file.csv"
DB_PATH = r"mydb.db"

# read the file once
tables = []
with open(r"D:\Claude_Plan\table_file.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        tables.append(row)

# ex5


"""cur.execute("select owner,count(*) from tables_info group by owner")
for row in cur.fetchall():
    print(row)


cur.execute("select name,rows_count from tables_info where rows_count between 10 and 300")
for row in cur.fetchall():
    print (row)"""

load_csv_to_db(CSV_PATH, DB_PATH)
report_by_owner(DB_PATH)
   
