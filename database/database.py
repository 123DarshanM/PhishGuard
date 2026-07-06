import sqlite3

DATABASE = "phishguard.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    CREATE TABLE IF NOT EXISTS email_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        email TEXT,

        score INTEGER,

        reasons TEXT,

        recommendations TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cur.execute("""

    CREATE TABLE IF NOT EXISTS url_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        url TEXT,

        score INTEGER,

        reasons TEXT,

        recommendations TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    conn.commit()

    conn.close()


# ==========================================
# SAVE EMAIL
# ==========================================

def save_email(

    email,

    score,

    reasons,

    recommendations

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO email_history(

        email,

        score,

        reasons,

        recommendations

    )

    VALUES(

        ?,?,?,?

    )

    """, (

        email,

        score,

        "\n".join(reasons),

        "\n".join(recommendations)

    ))

    conn.commit()

    conn.close()


# ==========================================
# SAVE URL
# ==========================================

def save_url(

    url,

    score,

    reasons,

    recommendations

):

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    INSERT INTO url_history(

        url,

        score,

        reasons,

        recommendations

    )

    VALUES(

        ?,?,?,?

    )

    """, (

        url,

        score,

        "\n".join(reasons),

        "\n".join(recommendations)

    ))

    conn.commit()

    conn.close()
# ==========================================
# EMAIL HISTORY
# ==========================================

def get_email_history():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM email_history

    ORDER BY created_at DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================
# URL HISTORY
# ==========================================

def get_url_history():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""

    SELECT *

    FROM url_history

    ORDER BY created_at DESC

    """)

    rows = cur.fetchall()

    conn.close()

    return rows


# ==========================================
# REPORT STATISTICS
# ==========================================

def report_stats():

    conn = get_connection()

    cur = conn.cursor()

    total_emails = cur.execute(

        "SELECT COUNT(*) FROM email_history"

    ).fetchone()[0]

    total_urls = cur.execute(

        "SELECT COUNT(*) FROM url_history"

    ).fetchone()[0]

    safe = cur.execute(

        "SELECT COUNT(*) FROM email_history WHERE score < 50"

    ).fetchone()[0]

    medium = cur.execute(

        "SELECT COUNT(*) FROM email_history WHERE score >= 50 AND score < 80"

    ).fetchone()[0]

    high = cur.execute(

        "SELECT COUNT(*) FROM email_history WHERE score >= 80"

    ).fetchone()[0]

    average = cur.execute(

        "SELECT ROUND(AVG(score),1) FROM email_history"

    ).fetchone()[0]

    if average is None:

        average = 0

    recent_emails = cur.execute("""

    SELECT

        id,

        email,

        score,

        created_at

    FROM email_history

    ORDER BY created_at DESC

    LIMIT 10

    """).fetchall()

    recent_urls = cur.execute("""

    SELECT

        id,

        url,

        score,

        created_at

    FROM url_history

    ORDER BY created_at DESC

    LIMIT 10

    """).fetchall()

    conn.close()
    return {

        "total_emails": total_emails,

        "total_urls": total_urls,

        "safe": safe,

        "medium": medium,

        "high": high,

        "average": average,

        "recent_emails": recent_emails,

        "recent_urls": recent_urls

    }


# ==========================================
# DASHBOARD STATISTICS
# ==========================================

def dashboard_stats():

    report = report_stats()

    return {

        "total_emails": report["total_emails"],

        "total_urls": report["total_urls"],

        "safe": report["safe"],

        "medium": report["medium"],

        "high": report["high"],

        "avg_score": report["average"],

        "average": report["average"],

        "recent_emails": report["recent_emails"],

        "recent_urls": report["recent_urls"]

    }


# ==========================================
# CLEAR DATABASE
# ==========================================

def clear_database():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("DELETE FROM email_history")

    cur.execute("DELETE FROM url_history")

    conn.commit()

    conn.close()
