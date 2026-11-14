from django.conf import settings
from django.db import connection


def query_sql(statement, params=None):
    """Run a query and return rows as a list of dicts."""
    with connection.cursor() as cursor:
        cursor.execute(statement, params or [])
        if cursor.description is None:
            return []
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
