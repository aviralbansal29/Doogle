from storage import models


def create_table():
    cur = models.con.cursor()
    cur.execute("DROP TABLE ChatHistory")
    models.con.commit()
    cur.execute("""CREATE TABLE ChatHistory
        (ID  SERIAL PRIMARY KEY         NOT NULL,
        DISCORD_MEMBER_ID   CHAR(30)    NOT NULL,
        SEARCH_DATA         CHAR(100)   NOT NULL);
    """)
    models.con.commit()
