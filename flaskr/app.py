from datetime import datetime

from flask import Flask, request, redirect, url_for, session, jsonify, Response, make_response
from flask_cors import CORS
from dotenv import load_dotenv
import os

from flaskr.config import db

from services.accounts import userToJSON, hasAdmin, validateLoginData
from services.admin import getEmployees, getReports, createAccount
from services.timecards import getTimecardsByUserDescending, timecardToJSON, getActiveTimecardByUser, addTimecardToUser, closeTimecard, timecard_getId

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
app.secret_key = os.getenv("SESSION_SECRET")


# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = validateLoginData(email, password)
    if user:
        session['user_id'] = user[0]
        resp = make_response(
            jsonify({'status': 'success', 'id': user[0], 'firstname': user[1], 'lastname': user[2], 'type': user[5]}))
        resp.headers['Access-Control-Expose-Headers'] = 'Set-Cookie'
        return resp
    else:
        return jsonify({
            'status': 'failed'
        })


@app.route('/create_acc', methods=["POST"])
def create_acc():
    if 'user_id' in session:
        if not hasAdmin(session['user_id']):
            return Response(status=401)

        createAccount(request)
    else:
        return Response(status=401)


@app.route('/dashboard')  # to add further info about current user
def dashboard():
    if 'user_id' in session:
        results = getTimecardsByUserDescending(session['user_id'])
        response = []
        for result in results:
            response.append(timecardToJSON(result))

        nextAction = 'checkout' if results[0][3] is None else 'checkin'

        return jsonify(resp=response, action=nextAction)
    else:
        return Response(status=401)


@app.route('/checkin', methods=["POST"])
def checkin():
    if 'user_id' in session:  # check if user is logged
        result = getActiveTimecardByUser(session['user_id'])
        if result is not None:  # check if user has already an active timecard
            return jsonify({"message": "You need to have the previous timecard closed in order to check-in again!", "error": 1})

        addTimecardToUser(session['user_id'])
        return jsonify({"message": "You checked-in successfully", "error": 0})
    else:
        return Response(status=401)


@app.route('/checkout', methods=["POST"])
def checkout():
    if 'user_id' in session:  # check if user is logged:
        activeTimecard = getActiveTimecardByUser(session['user_id'])
        if activeTimecard is None:
            return jsonify({"message": "You can't checkout without an active checkin", "error": 1})

        closeTimecard(timecard_getId(activeTimecard))
        return jsonify({"message": "You checked-out successfully", "error": 0})
    else:
        return Response(status=401)


@app.route('/employees', methods=["GET"])
def employees():
    if 'user_id' in session:
        if not hasAdmin(session['user_id']):
            return Response(status=401)

        results = getEmployees()

        response = []

        for result in results:
            response.append(userToJSON(result))

        return jsonify(resp=response)
    else:
        return Response(status=401)


@app.route('/reports', methods=["GET"])
def reports():
    if 'user_id' in session:
        if not hasAdmin(session['user_id']):
            return Response(status=401)

        return getReports()
    else:
        return Response(status=401)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=(os.getenv("ENVIRONMENT") != "PRODUCTION"), host="0.0.0.0", port=5000)
