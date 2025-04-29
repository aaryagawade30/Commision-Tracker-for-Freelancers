from flask import Flask, render_template, request, redirect, url_for
from db import get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM commission_table')
    commissions = cursor.fetchall()
    conn.close()
    return render_template('home.html', commissions=commissions)

@app.route('/client/<int:client_id>')
def client_details(client_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clients_table WHERE client_id = %s', (client_id,))
    client = cursor.fetchone()
    conn.close()
    return render_template('client.html', client=client)

@app.route('/payment/<int:commission_id>')
def payment_details(commission_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM payments_table WHERE commission_id = %s', (commission_id,))
    payments = cursor.fetchall()
    conn.close()
    return render_template('payment.html', payments=payments)

@app.route('/add_commission', methods=['GET', 'POST'])
def add_commission():
    if request.method == 'POST':
        client_id = request.form['client_id']
        description = request.form['description']
        start_date = request.form['start_date']
        due_date = request.form['due_date']
        amount = request.form['amount']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO commission_table (client_id, description, start_date, due_date, amount)
            VALUES (%s, %s, %s, %s, %s)
        ''', (client_id, description, start_date, due_date, amount))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clients_table')
    clients = cursor.fetchall()
    conn.close()
    return render_template('add_commission.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)
