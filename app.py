from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB_PATH = 'ecommerce.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # allows dict-like access
    return conn

# 1. List all customers
@app.route('/customers', methods=['GET'])
def list_customers():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Optional pagination
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))

    users = cursor.execute('SELECT * FROM users LIMIT ? OFFSET ?', (limit, offset)).fetchall()
    conn.close()

    return jsonify([dict(user) for user in users]), 200

# 2. Get specific customer details with order count
@app.route('/customers/<int:user_id>', methods=['GET'])
def customer_details(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if not user:
        return jsonify({'error': 'Customer not found'}), 404

    order_count = cursor.execute('SELECT COUNT(*) FROM orders WHERE user_id = ?', (user_id,)).fetchone()[0]
    conn.close()

    user_dict = dict(user)
    user_dict['order_count'] = order_count

    return jsonify(user_dict), 200

# 3. 404 fallback route
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

# Run server
if __name__ == '__main__':
    app.run(debug=True)
