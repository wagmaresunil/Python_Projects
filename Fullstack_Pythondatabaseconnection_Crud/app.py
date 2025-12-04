from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            database='sunil1',
            user='root',
            password='Wsunil@$1995'
        )
    except Error as e:
        print(f"DB Error: {e}")
        return None

@app.route('/')
def index():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY ID DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return render_template('index.html', users=users)
    return "Database connection failed!"

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            name = request.form['name']
            age = int(request.form['age'])
            city = request.form['city']
            cursor.execute("INSERT INTO users (NAME, AGE, CITY) VALUES (%s, %s, %s)", 
                         (name, age, city))
            conn.commit()
            cursor.close()
            conn.close()
            flash('User added successfully!')
            return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = get_db_connection()
    if not conn:
        return "Database error!"
    
    cursor = conn.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        city = request.form['city']
        cursor.execute("UPDATE users SET NAME=%s, AGE=%s, CITY=%s WHERE ID=%s", 
                      (name, age, city, user_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('User updated successfully!')
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM users WHERE ID=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        return render_template('edit.html', user=user)
    return "User not found!"

@app.route('/delete/<int:user_id>')
def delete_user(user_id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE ID=%s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('User deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)