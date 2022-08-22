import psycopg2
import psycopg2.extras


# crear conexion

#Global constanst

DB_HOST = "localhost"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASS = "123456"
DB_PORT = "5432"
    
#Connection
connection_address = """
host=%s port=%s user=%s password=%s dbname=%s
"""%(DB_HOST,DB_PORT,DB_USER,DB_PASS,DB_NAME)

# connection = psycopg2.connect(connection_address)
# conn = psycopg2.connect(connection_address)

# cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
# # #query
# SQL = "SELECT * FROM mydb.estacion"
# cursor.execute(SQL)

# #get values 
# all_values = cursor.fetchall()

# cursor.close()
# conn.close()
# print(' get values : ',all_values)

def get_connection():
    try:
        return psycopg2.connect(connection_address)