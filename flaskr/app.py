from flask import Flask, request, redirect, url_for, session, jsonify
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
        cursor.execute(f'SELECT a.id, a.firstname, a.lastname, t.check_in, t.check_out FROM accounts a JOIN timecards t ON t.account_id = {session['user_id']} WHERE a.id = {session['user_id']} GROUP BY a.id')
        timecards = cursor.fetchall()
        cursor.close()
        return timecards
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
