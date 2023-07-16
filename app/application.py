""" TP CI/CD Flask app """
import os
import json
import psycopg2
from flask import Flask, request
from prometheus_client import Counter, generate_latest

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



http_requests_total = Counter('http_requests_total', 'Requests to city API', ['method', 'code'])

cur.execute("select exists(select * from information_schema.tables where table_name='city')")
if not cur.fetchone()[0]:
    cur.execute("CREATE TABLE city (id SERIAL PRIMARY KEY,department_code character varying(255) NOT NULL,insee_code character varying(255),zip_code character varying(255),name character varying(255) NOT NULL,lat float NOT NULL,lon float NOT NULL );")
    cur.execute("INSERT INTO city (department_code, insee_code, zip_code, name, lat, lon)VALUES ('01', '01001', '01400', 'L''Abergement-Clémenciat', 46.15678199203189, 4.92469920318725),('01', '01002', '01640', 'L''Abergement-de-Varey', 46.01008562499999, 5.42875916666667),('01', '01004', '01500', 'Ambérieu-en-Bugey', 45.95840939226519, 5.3759920441989),('01', '01005', '01330', 'Ambérieux-en-Dombes', 46.00012039215686, 4.9106016993464);")

@app.route("/_health")
def health():
    """ Healthcheck """
    http_requests_total.labels(
        method='get',
        code=204).inc()
    return "", 204


@app.route('/metrics')
def metrics():
    """ Metrics """
    return generate_latest()


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
            http_requests_total.labels(
                method='post',
                code=500).inc()
            return str(err2), 500

        http_requests_total.labels(
            method='post',
            code=201).inc()
        return "", 201

    try:
        # Execute a query
        cur.execute("SELECT * FROM city")

        # Retrieve query results
        cities = cur.fetchall()
    except Exception as err3:
        http_requests_total.labels(
            method='get',
            code=500).inc()
        return str(err3), 500

    http_requests_total.labels(
        method='get',
        code=200).inc()
    return json.dumps(cities), 200


if __name__ == '__main__':
    app.run(host=CITY_API_ADDR, port=CITY_API_PORT)
