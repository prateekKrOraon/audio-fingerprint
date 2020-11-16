from legacy.constants import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import pymysql


def get_conn(args):
    """MySQL connection.

    Connects the MySQL database in server (localhost/remote).

    Args:
        args:
            Either 'localhost' to connect to localhost server or 'remote'

    Returns:
        list: Contains connection object and cursor.
    """

    if args == 'localhost':
        conn = pymysql.connect("localhost", "root", "", "song_identifier")
    elif args == 'remote':
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB
        )

    return [conn, conn.cursor()]
