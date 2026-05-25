import re

BLOCKED_KEYWORDS = [
    "INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE",
    "REPLACE", "GRANT", "REVOKE", "MERGE", "CALL", "EXEC", "COPY"
]


def validate_sql(sql_query: str) -> bool:
    query = sql_query.strip()
    query_upper = query.upper()

    if not query_upper.startswith("SELECT"):
        return False

    # Block multiple statements. One semicolon at the end is okay.
    if ";" in query[:-1]:
        return False

    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", query_upper):
            return False

    return True
