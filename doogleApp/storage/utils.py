from storage import models


def create_table():
    """
    Create table, throws error if exists
    """
    cur = models.con.cursor()
    cur.execute("""CREATE TABLE ChatHistory
        (ID  SERIAL PRIMARY KEY         NOT NULL,
        DISCORD_MEMBER_ID   CHAR(30)    NOT NULL,
        SEARCH_DATA         CHAR(100)   NOT NULL,
        CREATED_AT          TIMESTAMP   NOT NULL);
    """)
    cur.execute("ALTER TABLE ChatHistory ALTER COLUMN CREATED_AT SET DEFAULT now();")
    cur.execute("""ALTER TABLE ChatHistory ADD "document_vectors" tsvector;
    CREATE INDEX idx_doc_vec ON ChatHistory USING gin(document_vectors);""")
    models.con.commit()


def recreate_table():
    """
    Recreate the table
    """
    cur = models.con.cursor()
    cur.execute("DROP TABLE ChatHistory;")
    create_table()
