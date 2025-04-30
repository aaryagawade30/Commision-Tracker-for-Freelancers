from flask import Flask, render_template, request, redirect, url_for, jsonify
from db import get_db_connection
import os
import json
import datetime

app = Flask(__name__)
app.static_folder = 'static'

# Custom JSON encoder to handle date objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

app.json_encoder = CustomJSONEncoder

# Ensure static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    # Make sure your HTML file is in the templates folder
    return render_template('final.html')

@app.route('/get_clients')
def get_clients():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM clients_table')
    clients = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clients)

@app.route('/get_commissions')
def get_commissions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        # Use LEFT JOIN to ensure we get commissions even if client lookup fails
        cursor.execute('''
            SELECT c.*, CONCAT(COALESCE(cl.first_name, ''), ' ', COALESCE(cl.last_name, '')) AS client_name
            FROM commission_table c
            LEFT JOIN clients_table cl ON c.client_id = cl.client_id
        ''')
        commissions = cursor.fetchall()
        print(f"Fetched {len(commissions)} commissions")
        cursor.close()
        conn.close()
        return jsonify(commissions)
    except Exception as e:
        print(f"Error in get_commissions: {str(e)}")
        return jsonify([])  # Return empty array on error

@app.route('/get_payments')
def get_payments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM payments_table')
        payments = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(payments)
    except Exception as e:
        print(f"Error in get_payments: {str(e)}")
        return jsonify([])  # Return empty array on error

@app.route('/add_client', methods=['POST'])
def add_client():
    try:
        client_id = request.form['client_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO clients_table (client_id, first_name, last_name, email, phone_number)
            VALUES (%s, %s, %s, %s, %s)
        ''', (client_id, first_name, last_name, email, phone_number))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/add_commission', methods=['POST'])
def add_commission():
    try:
        commission_id = request.form['commission_id']
        client_id = request.form['client_id']
        description = request.form['description']
        start_date = request.form['start_date']
        due_date = request.form['due_date']
        artwork_status = request.form['artwork_status']
        amount = request.form['amount']
        payment_status = request.form['payment_status']
        final_delivery_date = request.form.get('final_delivery_date')
        
        # Handle empty string for final_delivery_date
        if final_delivery_date == '':
            final_delivery_date = None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO commission_table (commission_id, client_id, description, start_date, due_date, 
                                        artwork_status, amount, payment_status, final_delivery_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (commission_id, client_id, description, start_date, due_date, 
              artwork_status, amount, payment_status, final_delivery_date))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/add_payment', methods=['POST'])
def add_payment():
    try:
        payment_id = request.form['payment_id']
        commission_id = request.form['commission_id']
        payment_date = request.form['payment_date']
        amount_paid = request.form['amount_paid']
        amount_remaining = request.form['amount_remaining']
        payment_method = request.form['payment_method']
        payment_status = request.form['payment_status']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO payments_table (payment_id, commission_id, payment_date, amount_paid, 
                                      amount_remaining, payment_method, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', (payment_id, commission_id, payment_date, amount_paid, 
              amount_remaining, payment_method, payment_status))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_client/<client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM clients_table WHERE client_id = %s', (client_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_commission/<commission_id>', methods=['DELETE'])
def delete_commission(commission_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM commission_table WHERE commission_id = %s', (commission_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

@app.route('/delete_payment/<payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM payments_table WHERE payment_id = %s', (payment_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)