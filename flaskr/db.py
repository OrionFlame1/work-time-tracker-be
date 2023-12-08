import mysql.connector

def init_db():
    mydb = mysql.connector.connect(
      host="database",
      user="root",
      password="mata",
      database="work_time_tracker"
    )

    return mydb