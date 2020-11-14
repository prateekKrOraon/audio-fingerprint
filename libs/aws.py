from legacy.constants import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import pymysql


def get_conn():
    """MySQL connection.

    Connects the MySQL database in AWS server.

    Returns:
        list: Contains connection object and cursor.
    """
    
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB
    )

    return [conn, conn.cursor()]
