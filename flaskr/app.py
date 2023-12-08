from flask import Flask, request, redirect, url_for, session, jsonify
import db

app = Flask(__name__)

mydb = db.init_db()

# Set a secret key for session management
app.secret_key = 'W4Qr2R7MB7'

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({'status': 'success', 'id': user[0], 'firstname': user[1], 'lastname': user[2], 'type': user[5]})
        # return redirect(url_for('dashboard'))
    else:
        return jsonify({
            'status': 'failed'
        })

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return f'Welcome, User {session["user_id"]}!'
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
