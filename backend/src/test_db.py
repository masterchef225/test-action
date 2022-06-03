import MySQLdb

db = MySQLdb.connect(
    host="mysql",
    port=3306,
    user="test",
    passwd="test",
    db="gmop",
)

cursor = db.cursor()
cursor.execute("SELECT VERSION()")
results = cursor.fetchone()

print(f'version {results}')