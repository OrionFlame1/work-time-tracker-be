from flask import jsonify, Response

from flaskr.config import db

db = db.init_db()


def getEmployees():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM accounts WHERE type = 'employee'")
    result = cursor.fetchall()

    cursor.close()
    return result


def getReports():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM timecards")
    totalTimecards = cursor.fetchall()

    cursor.execute("SELECT * FROM accounts")
    totalAccounts = cursor.fetchall()

    cursor.execute("SELECT * FROM accounts WHERE id IN(SELECT timecards.account_id FROM timecards)")
    accountsWithTimecards = cursor.fetchall()

    cursor.close()
    return jsonify({
        "totalTimecards": len(totalTimecards),
        "totalAccounts": len(totalAccounts),
        "accountsWithTimecards": len(accountsWithTimecards)
    })


def createAccount(req):
    cursor = db.cursor()
    data = req.get_json()
    firstname = data['firstname']
    lastname = data['lastname']
    email = data['email']
    password = data['password']
    cursor.execute(
        f'INSERT INTO accounts SET firstname = {firstname}, lastname = {lastname}, email = {email}, password = {password}')

    cursor.close()
    return Response(status=201)
