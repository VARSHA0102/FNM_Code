from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = '456+'  # Ensure this is securely generated for production use

# Database configuration (create the connection globally, but cursor within routes)
def get_log_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="Demo",
            password="12345678",
            database="LogFNM"
        )
        if db.is_connected():
            return db
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None


# Decorator to require login for specific routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:  # Check if user is logged in
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function


# Route for the homepage (renders login/signup page)
@app.route('/')
def home():
    username = session.get('username')  # Get the username from the session if logged in
    return render_template('index.html', username=username)


# Route for rendering the login page
@app.route('/login')
def login_page():
    return render_template('login.html')


# Route for handling signup form submission
@app.route('/signup', methods=['POST'])
def signup():
    db = get_log_db_connection()
    if db is None:
        flash("Database connection error.", "danger")
        return redirect(url_for('home'))

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()

    # Check if the email already exists
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user:
        flash('Email already registered. Please login.', 'danger')
        db.close()
        return redirect(url_for('home'))

    # Insert new user into the database
    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, email, password))
    db.commit()

    flash('Account created successfully!', 'success')
    db.close()
    return redirect(url_for('login_page'))


# Route for handling login form submission
@app.route('/login', methods=['POST'])
def login():
    db = get_log_db_connection()
    if db is None:
        flash("Database connection error.", "danger")
        return redirect(url_for('home'))

    email = request.form.get('email')
    password = request.form.get('password')

    cursor = db.cursor()

    # Check if the user exists in the database
    query = "SELECT * FROM users WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    user = cursor.fetchone()

    if user:
        # Store the user's name in the session
        session['username'] = user[1]  # Assuming the second field is the username
        flash('Logged in successfully!', 'success')
        db.close()
        return redirect(url_for('home'))  # Redirect to index.html after login
    else:
        flash('Invalid credentials, please try again.', 'danger')
        db.close()
        return redirect(url_for('login_page'))


# Route to handle logout
@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from the session
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))


# Route for rendering form detail page after signup (protected route)
@app.route('/contact')
@login_required
def contact():
    return render_template('contact.html')


# Protected route: Assessment page, only accessible after login
@app.route('/ass')
@login_required
def ass():
    return render_template('ass.html')

db_config = {
    'user': 'Demo',
    'password': '12345678',
    'host': 'localhost',
    'database': 'LogFNM'
}

# Cleanup database connection after request
@app.teardown_appcontext
def close_connection(exception):
    db = get_log_db_connection()
    if db is not None:
        db.close()

@app.route('/submit', methods=['POST'])
def submit_assessment():
    name = request.form['name']
    email = request.form['email']
    assid = request.form['assid']
    file = request.files['file']

    # Check if file is a ZIP file
    if file and file.filename.endswith('.zip'):
        # Save the file
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Insert submission data into the MySQL database
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            query = "INSERT INTO submissions (name, email, assid, file_name) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (name, email, assid, file.filename))
            connection.commit()

        except mysql.connector.Error as err:
            flash(f"Error: {err}")
            return redirect(url_for('ass'))
        finally:
            cursor.close()
            connection.close()

        flash(f"Thank you {name}, your assessment has been submitted successfully!")
        return redirect(url_for('home'))  # Redirect to the homepage after submission

    else:
        flash("Please upload a valid ZIP file.")
        return redirect(url_for('ass'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)

