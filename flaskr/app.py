import json
from datetime import datetime

from flask import Flask, request, redirect, url_for, session, jsonify, make_response
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

mydb = db.init_db()

# Set a secret key for session management
app.secret_key = 'W4Qr2R7MB7'

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    # data = request.form
    email = request.form.get('email')
    password = request.form.get('password')

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        session['user_id'] = user[0]
        return jsonify({'status': 'success', 'id': user[0], 'firstname': user[1], 'lastname': user[2], 'type': user[5]})
        # return redirect(url_for('dashboard'))
    else:
        return jsonify({
            'status': 'failed'
        })

@app.route('/dashboard') # to add further info about current user
def dashboard():
    if 'user_id' in session:
        cursor = mydb.cursor()
        cursor.execute(f'SELECT * FROM timecards JOIN accounts on timecards.account_id = accounts.id WHERE timecards.account_id = {session['user_id']}')
        results = cursor.fetchall()
        cursor.close()
        response = []
        for result in results:
            response.append({'id': result[0],
                                     'check_in': datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S'),
                                     'check_out': datetime.strptime(str(result[3]), '%Y-%m-%d %H:%M:%S'),
                                     'full_name': f'{result[5]} {result[6]}'})
        return jsonify(resp=response)
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
