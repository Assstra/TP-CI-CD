from flask import Flask, request
import psycopg2
import json

app = Flask(__name__)

conn = 0

try: 
    #Establishing the database connection
    conn = psycopg2.connect(
    database="city_api", user='test', password='test', host='127.0.0.1', port='5435'
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