from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # ✅ Allow frontend requests

DB_PATH = 'ecommerce.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/customers', methods=['GET'])
def list_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    users = cursor.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, offset)).fetchall()

    # add order count for each user
    result = []
    for user in users:
        order_count = cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (user['id'],)).fetchone()[0]
        user_dict = dict(user)
        user_dict['order_count'] = order_count
        result.append(user_dict)

    conn.close()
    return jsonify(result), 200

@app.route('/customers/<int:user_id>', methods=['GET'])
def customer_details(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({'error': 'Customer not found'}), 404

    order_count = cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (user_id,)).fetchone()[0]
    user_dict = dict(user)
    user_dict['order_count'] = order_count

    conn.close()
    return jsonify(user_dict), 200

@app.route('/customers/<int:customer_id>/orders', methods=['GET'])
def get_customer_orders(customer_id):
    conn = get_db_connection()

    customer = conn.execute('SELECT * FROM users WHERE id = ?', (customer_id,)).fetchone()
    if not customer:
        conn.close()
        return jsonify({'error': 'Customer not found'}), 404

    orders = conn.execute('SELECT * FROM orders WHERE user_id = ?', (customer_id,)).fetchall()
    conn.close()

    return jsonify([dict(order) for order in orders]), 200

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order_details(order_id):
    conn = get_db_connection()
    order = conn.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
    conn.close()

    if not order:
        return jsonify({'error': 'Order not found'}), 404

    return jsonify(dict(order)), 200

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)  # ✅ must run on localhost for React
