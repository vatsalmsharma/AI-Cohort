import psycopg2
import os

# Refactored - Comment 
# conn = psycopg2.connect(database = "AI_COHORT", 
#                         user = "vatsal", 
#                         host= 'localhost',
#                         password = "vatsal_postgres14",
#                         port = 5432)

# Refactored
# Read env vars (with sensible defaults for local dev)
DB_NAME = os.getenv("DB_NAME", "AI_COHORT")
DB_USER = os.getenv("DB_USER", "vatsal")
DB_PASSWORD = os.getenv("DB_PASSWORD", "vatsal_postgres14")
DB_HOST = os.getenv("DB_HOST", "localhost")   # <- will be "pgdatabase" inside Docker
DB_PORT = int(os.getenv("DB_PORT", "5432"))

# Create connection
conn = psycopg2.connect(
    database=DB_NAME,
    user=DB_USER,
    host=DB_HOST,
    password=DB_PASSWORD,
    port=DB_PORT
)

# Open a cursor to perform database operations
cur = conn.cursor()

conn.autocommit = True

print(f"Connected to DB at {DB_HOST}:{DB_PORT} as {DB_USER}")