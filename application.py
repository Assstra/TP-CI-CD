from flask import Flask, request
import os
import psycopg2
import json
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = 0

CITY_API_ADDR = os.getenv("CITY_API_ADDR", default='0.0.0.0')
CITY_API_PORT = os.getenv("CITY_API_PORT", default='2022')
CITY_API_DB_PORT = os.getenv("CITY_API_DB_PORT")
CITY_API_DB_USER = os.getenv("CITY_API_DB_USER")
CITY_API_DB_PWD = os.getenv("CITY_API_DB_PWD")

if not CITY_API_DB_PORT or not CITY_API_DB_USER or not CITY_API_DB_PWD:
    raise ValueError("Missing database configuration env variables")

try: 
    #Establishing the database connection
    conn = psycopg2.connect(
    database="city_api", user=CITY_API_DB_USER, password=CITY_API_DB_PWD, host="db", port=CITY_API_DB_PORT
    )
except Exception as err:
    print(err)
    raise RuntimeError("Cannot connect to the database")

# Open a cursor to perform database operations
cur = conn.cursor()

@app.route("/_health")
def health():
    return "",204

@app.route("/city", methods=['POST', 'GET'])
def city():
    if request.method == 'POST':
        try:
            data = request.json
            cur.execute("INSERT INTO city (department_code, insee_code, zip_code, name, lat, lon) VALUES (%s, %s, %s, %s, %s, %s)",
            (data.get('department_code'), data.get('insee_code'), data.get('zip_code'), data.get('name'), data.get('lat'), data.get('lon')))
            conn.commit()
        except Exception as err:
            return str(err), 500
        return "", 201
    else:
        try:
            # Execute a query
            cur.execute("SELECT * FROM city")

            # Retrieve query results
            cities = cur.fetchall()
        except Exception as err:
            return str(err), 500
        return json.dumps(cities), 200

if __name__ == '__main__':
    app.run(host=CITY_API_ADDR, port=CITY_API_PORT)