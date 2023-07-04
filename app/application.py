""" TP CI/CD Flask app """
import os
import json
import psycopg2
from flask import Flask, request

app = Flask(__name__)

conn = 0

CITY_API_ADDR = os.environ.get("CITY_API_ADDR", default='127.0.0.1')
CITY_API_PORT = os.environ.get("CITY_API_PORT", default='2022')
CITY_API_DB_PORT = os.environ.get("CITY_API_DB_PORT", default='5435')
CITY_API_DB_URL = os.environ.get("CITY_API_DB_URL")
CITY_API_DB_USER = os.environ.get("CITY_API_DB_USER")
CITY_API_DB_PWD = os.environ.get("CITY_API_DB_PWD")

if not CITY_API_DB_URL or not CITY_API_DB_USER or not CITY_API_DB_PWD:
    raise ValueError("Missing database configuration env variables")

try:
    # Establishing the database connection
    conn = psycopg2.connect(
        database="city_api",
        user=CITY_API_DB_USER,
        password=CITY_API_DB_PWD,
        host=CITY_API_DB_URL,
        port=CITY_API_DB_PORT
    )

except Exception as err1:
    raise RuntimeError("Cannot connect to the database") from err1

# Open a cursor to perform database operations
cur = conn.cursor()


@app.route("/_health")
def health():
    """ Healthcheck """
    return "", 204


@app.route("/city", methods=['POST', 'GET'])
def city():
    """ Get or insert cities """
    if request.method == 'POST':
        try:
            data = request.json
            cur.execute(
                "INSERT INTO city (department_code, insee_code, zip_code, name, lat, lon)" +
                " VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    data.get('department_code'),
                    data.get('insee_code'),
                    data.get('zip_code'),
                    data.get('name'),
                    data.get('lat'),
                    data.get('lon')
                ))
            conn.commit()
        except Exception as err2:
            return str(err2), 500
        return "", 201

    try:
        # Execute a query
        cur.execute("SELECT * FROM city")

        # Retrieve query results
        cities = cur.fetchall()
    except Exception as err3:
        return str(err3), 500
    return json.dumps(cities), 200


if __name__ == '__main__':
    app.run(host=CITY_API_ADDR, port=CITY_API_PORT)
