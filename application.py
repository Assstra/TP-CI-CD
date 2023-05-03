from flask import Flask, request
import psycopg2
import json

app = Flask(__name__)

#Establishing the database connection
conn = psycopg2.connect(
   database="mydb", user='postgres', password='password', host='127.0.0.1', port= '5432'
)

# Open a cursor to perform database operations
cur = conn.cursor()



@app.route("/_health")
def health():
    return "",204

@app.route("/city", methods=['POST', 'GET'])
def city():
    if request.method == 'POST':
        cur.execute("INSERT INTO city (c1, c2, c3) VALUES(%s, %s, %s)", (1, 2, 3))
        conn.commit()
        return "", 201
    else:
        # Execute a query
        cur.execute("SELECT * FROM city")

        # Retrieve query results
        cities = cur.fetchall()
        return json.dumps(cities), 200