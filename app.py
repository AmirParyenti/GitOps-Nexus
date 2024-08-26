from flask import Flask, request, render_template
import psycopg2
from psycopg2.extras import DictCursor
import os

#  glpat-Z-tqKo245DLdMvZA5p2u - cred aabb

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'my-postgresql.db.svc.cluster.local'),
        database=os.getenv('DATABASE_NAME', 'postgres'),
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD'),
        port=os.getenv('DATABASE_PORT', '5432')  
    )
    return conn

def create_table():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            second_name VARCHAR(255) NOT NULL,
            age INTEGER NOT NULL,
            id_number VARCHAR(255) NOT NULL UNIQUE,
            city VARCHAR(255) NOT NULL
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    second_name = request.form['second_name']
    age = request.form['age']
    id_number = request.form['id_number']
    city = request.form['city']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, second_name, age, id_number, city) VALUES (%s, %s, %s, %s, %s)',
                (name, second_name, age, id_number, city))
    conn.commit()
    cur.close()
    conn.close()
    return 'User added successfully'

@app.route('/search', methods=['POST'])
def search():
    search_name = request.form['search_name']
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=DictCursor)  
    cur.execute('SELECT * FROM users WHERE name = %s', (search_name,))
    users = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('results.html', users=users)

if __name__ == '__main__':
    create_table()  # Call create_table function to ensure table exists on start
    app.run(host='0.0.0.0', port=5000)
