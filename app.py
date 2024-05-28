from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__, template_folder='/var/www/html/')
CORS(app)

# Function to create a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="private_ip_data_tier_instance",
            user="flaskuser",
            password="admin",
            database="flaskdb"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Function to insert data into the database
def insert_data(connection, first_name, last_name, dob, email):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO applications (first_name, last_name, dob, email) VALUES (%s, %s, %s, %s)", (first_name, last_name, dob, email))
    connection.commit()
    cursor.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        dob = request.form['dob']
        email = request.form['email']

        connection = create_connection()
        if connection:
            insert_data(connection, first_name, last_name, dob, email)
            connection.close()
            return jsonify({'success': True, 'message': 'Application submitted successfully'})
        else:
            return jsonify({'success': False, 'message': 'Database connection failed'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
