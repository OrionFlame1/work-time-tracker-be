from datetime import datetime

from flask import Flask, request, redirect, url_for, session, jsonify, Response, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os

import db

load_dotenv()
app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)
CORS(app, supports_credentials=True)

mydb = db.init_db()

# Set a secret key for session management
app.secret_key = 'W4Qr2R7MB7'

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    # data = request.form
    # email = request.form.get('email')
    # password = request.form.get('password')
    data = request.get_json()
    email = data['email']
    password = data['password']

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['user_id'] = user[0]
        resp = make_response(jsonify({'status': 'success', 'id': user[0], 'firstname': user[1], 'lastname': user[2], 'type': user[5]}))
        resp.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
        return resp
        # return redirect(url_for('dashboard'))
    else:
        return jsonify({
            'status': 'failed'
        })

@app.route('/dashboard') # to add further info about current user
def dashboard():
    print(request.headers)
    if 'user_id' in session:
        cursor = mydb.cursor()
        cursor.execute(f'SELECT * FROM timecards JOIN accounts on timecards.account_id = accounts.id WHERE timecards.account_id = {session['user_id']} ORDER BY timecards.check_in DESC')
        results = cursor.fetchall()
        cursor.close()
        response = []
        for result in results:
            response.append({'id': result[0],
                                     'check_in': datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S'),
                                     'check_out': datetime.strptime(str(result[3]), '%Y-%m-%d %H:%M:%S'),
                                     'full_name': f'{result[5]} {result[6]}'})
        try:
            if results[0][3] is None: # value that indicates if the checkout button shall be shown instead of the checkin one
                response.append({'action': 'checkout'})
            else:
                response.append({'action': 'checkin'})
        except IndexError:
            response.append({'action': 'checkin'})
        return jsonify(resp=response)
    else:
        return redirect(url_for('login'))

@app.route('/admin', methods=["GET"]) # to add further info about current user
def admin():
    if 'user_id' in session:
        cursor = mydb.cursor()
        cursor.execute(f'SELECT type FROM accounts WHERE id = {session['user_id']}')
        type = cursor.fetchone()[0]
        if type == "admin":
            # return jsonify({'message': 'admin'})
            resp = []
            cursor.execute(f'SELECT id, firstname, lastname, email, type FROM accounts WHERE id = {session['user_id']}') # getting data to show about current logged admin
            current_user = cursor.fetchone()
            resp.append({"info": current_user})
            cursor.execute(f'SELECT id, firstname, lastname, email, type FROM accounts WHERE NOT id = {session['user_id']}')
            accounts = cursor.fetchall()
            resp.append({"accounts": accounts})
            cursor.execute(f'SELECT t.id, t.account_id, t.check_in, t.check_out FROM timecards t JOIN accounts ON t.account_id = accounts.id')
            timecards = cursor.fetchall()
            resp.append({"timecards": timecards})
            return jsonify(resp=resp)

        return jsonify({"message": "fail"})
    else:
        return redirect(url_for('login'))

@app.route('/checkin', methods=["POST"])
def checkin():
    if 'user_id' in session: # check if user is logged
        cursor = mydb.cursor()
        cursor.execute(f'SELECT * FROM timecards WHERE account_id = {session['user_id']} ORDER BY check_in DESC LIMIT 1') # check if current user has an active checkin
        result = cursor.fetchone()
        try:
            if result[3] is None: # check if the last timecards has a checkout not null
                return jsonify({"message": "You can't check-in with another active check-in. Check-out first!", "error": 1})
        finally:
            cursor.execute(f"INSERT INTO timecards SET account_id = {session['user_id']}, check_in = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}'")
            return jsonify({"message": "You checked-in successfully", "error": 0})
    else:
        return redirect(url_for('login'))

@app.route('/checkout', methods=["POST"])
def checkout():
    if 'user_id' in session: # check if user is logged:
        cursor = mydb.cursor()
        cursor.execute(f'SELECT * FROM timecards WHERE account_id = {session['user_id']} ORDER BY check_in DESC LIMIT 1')  # check if current user has an active checkin
        result = cursor.fetchone()
        try:
            if result[3] is None:  # check if the last timecards has a checkout not null
                cursor.execute(f"UPDATE timecards SET check_out = '{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}' WHERE account_id = {session['user_id']}")
                return jsonify({"message": "You checked-out successfully", "error": 0})
        finally:
            return jsonify({"message": "You can't checkout without an active checkin", "error": 1})
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/create_acc', methods=["POST"])
def create_acc():
    if 'user_id' in session:
        cursor = mydb.cursor()
        cursor.execute(f'SELECT type FROM accounts WHERE id = {session['user_id']}')  # check if current user has an active checkin
        result = cursor.fetchone()[0]
        if result == "admin":
            data = request.get_json()
            firstname = data['firstname']
            lastname = data['lastname']
            email = data['email']
            password = data['password']
            # try:

            if data['type'] is not None:
                type = data['type']
            else:
                type = "employee"
            cursor.execute(f"INSERT INTO accounts SET firstname = '{firstname}', lastname = '{lastname}', email = '{email}', password = '{password}', type = '{type}'")
            print("created")
            return jsonify({"message": "Account created successfully", "error": 0})
        print("fail admin")
        return jsonify({"message": "Use an admin account to create a new account", "error": 1})
    else:
        print("fail login")
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=(os.getenv("ENVIRONMENT") != "PRODUCTION"), host="0.0.0.0", port=5000)
