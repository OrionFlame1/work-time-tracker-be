from datetime import datetime

from flaskr.config import db

db = db.init_db()


def getTimecardsByUserDescending(userId):
    cursor = db.cursor()
    cursor.execute(
        f'SELECT * FROM timecards JOIN accounts on timecards.account_id = accounts.id WHERE timecards.account_id = {userId} ORDER BY timecards.check_in DESC')
    results = cursor.fetchall()
    cursor.close()

    return results


def getActiveTimecardByUser(userId):
    cursor = db.cursor()
    cursor.execute(
        f'SELECT * FROM timecards WHERE account_id = {userId} AND check_out IS NULL')
    result = cursor.fetchone()
    cursor.close()

    return result


def addTimecardToUser(userId):
    cursor = db.cursor()
    cursor.execute(f'INSERT INTO timecards(account_id, check_in) VALUES({userId}, CURRENT_TIMESTAMP())')
    cursor.close()


def closeTimecard(timecardId):
    cursor = db.cursor()
    cursor.execute(
        f'UPDATE timecards SET check_out = CURRENT_TIMESTAMP() WHERE id = {timecardId}')
    cursor.close()


def timecardToJSON(result):
    return {'id': result[0],
            'check_in': datetime.strptime(str(result[2]), '%Y-%m-%d %H:%M:%S') if result[2] is not None else None,
            'check_out': datetime.strptime(str(result[3]), '%Y-%m-%d %H:%M:%S') if result[3] is not None else None,
            'full_name': f'{result[5]} {result[6]}'}


def timecard_getId(result):
    return result[0]
