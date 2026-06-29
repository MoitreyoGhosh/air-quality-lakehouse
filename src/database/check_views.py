from src.database.connection import get_connection

con = get_connection()

views = con.execute("""

SELECT table_name

FROM information_schema.views

ORDER BY table_name

""").fetchdf()

print(views)

con.close()