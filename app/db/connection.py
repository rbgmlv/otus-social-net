import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config


def get_connection():
    """Соединение с БД."""
    return psycopg2.connect(**Config.get_db_config())


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Выполнение параметризорванного SQL-запроса.

    Args:
        query: SQL-запрос с плейсхолдерами
        params: кортеж с параметрами
        fetch_one: возвращение одной записи
        fetch_all: возвращение всех записей
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)

            if fetch_one:
                result = cur.fetchone()
            elif fetch_all:
                result = cur.fetchall()
            else:
                result = None

            conn.commit()
            return result
    except Exception as e:
        if conn:
            conn.rollback()
        raise eexecute_query
    finally:
        if conn:
            conn.close()
