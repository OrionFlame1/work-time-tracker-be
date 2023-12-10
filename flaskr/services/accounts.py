from flaskr.config import db

db = db.init_db()


def getRoleByUserId(userId):
    cursor = db.cursor()
    cursor.execute(f'SELECT type FROM accounts WHERE id = {userId}')
    result = cursor.fetchone()[0]

    cursor.close()
    return result


def userToJSON(result):
    return {
        "id": result[0],
        "firstname": result[1],
        "lastname": result[2],
        "role": result[5],
        "email": result[4]
    }


def hasAdmin(userId):
    userRole = getRoleByUserId(userId)
    return userRole == 'admin'


def validateLoginData(email, password):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM accounts WHERE email = %s AND password = %s', (email, password))
    user = cursor.fetchone()
    cursor.close()

    return user

