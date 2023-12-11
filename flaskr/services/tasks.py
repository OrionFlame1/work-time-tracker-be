from flaskr.config import db

db = db.init_db()


def createTask(userId, name, description):
    cursor = db.cursor()
    cursor.execute(
        f'INSERT INTO tasks(account_id, task_name, task_desc, status, created_at) VALUES ({userId if userId is not None else 'NULL'}, \'{name}\', {'\'description\'' if description is not None else 'NULL'}, \'unassigned\', CURRENT_TIMESTAMP()) RETURNING id, account_id, task_name, task_desc, status, created_at')
    result = cursor.fetchone()
    cursor.close()

    return result

def updateTask(taskId, userId, name, description, status, finish):
    arrayedData = []

    if userId is not None:
        arrayedData.append(f'account_id = {userId}')
    if name is not None:
        arrayedData.append(f'task_name = \'{name}\'')
    if description is not None:
        arrayedData.append(f'task_desc = \'{description}\'')
    if status is not None:
        arrayedData.append(f'status = \'{status}\'')
    if finish is True:
        arrayedData.append('finished_at = CURRENT_TIMESTAMP()')

    cursor = db.cursor()
    cursor.execute(f'UPDATE tasks SET {', '.join(arrayedData)} WHERE id = {taskId}')
    cursor.close()

def taskToJSON(result):
    return {
        "id": result[0],
        "assignedTo": result[1],
        "name": result[2],
        "description": result[3],
        "status": result[4],
        "created_at": result[5]
    }