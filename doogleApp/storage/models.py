import os
import psycopg2

con = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOSTNAME"),
    port=os.getenv("DB_PORT")
)


(HI_COMMAND, SEARCH_COMMAND, HISTORY_COMMAND, UNKNOWN_COMMAND) = range(4)


class ChatHistory:

    def __init__(self, discord_member_id, search_data=None):
        self.discord_member_id = discord_member_id
        self.search_data = search_data
        self.cur = con.cursor()

    def clean(self):
        """
        Basic Validations
        """
        # Validate required fields
        if not self.discord_member_id:
            raise ValueError("discord_member_id is required")

        if not self.search_data:
            raise ValueError("search_data is required")

        # Validate data type
        if type(self.discord_member_id) != int:
            raise ValueError("Invalid discord_member_id")

        if type(self.search_data) != str:
            raise ValueError("Invalid search_data")

    def insert(self):
        """
        Insert new data into Database
        """
        self.clean()
        self.cur.execute(f"""
        INSERT INTO {self.__class__.__name__}
        (DISCORD_MEMBER_ID,SEARCH_DATA,document_vectors)
        VALUES ('{self.discord_member_id}','{self.search_data}',to_tsvector('{self.search_data}'));
        """)
        con.commit()

    def filter(self, text, fields=("SEARCH_DATA", ), limit=5):
        """
        Retrieve data from database
        :param text: (String) text to be searched
        :param fields: fields to be retrieved
        :param limit: LIMIT query
        :return: search data
        """
        self.cur.execute(f"""
        SELECT {",".join(fields)} FROM ChatHistory
        WHERE DISCORD_MEMBER_ID='{self.discord_member_id}' AND SEARCH_DATA LIKE '%{text}%'
        ORDER BY CREATED_AT DESC
        LIMIT {limit};
        """)
        return self.cur.fetchall()

    def quick_filter(self, text, fields=("SEARCH_DATA", ), limit=5):
        """
        Retrieve data using vector search
        :param text: (String) text to be searched
        :param fields: fields to be retrieved
        :param limit: LIMIT query
        :return: search data
        """
        self.cur.execute(f"""
        SELECT {",".join(fields)} FROM ChatHistory
        WHERE DISCORD_MEMBER_ID='{self.discord_member_id}' AND document_vectors @@ to_tsquery('{text}')
        ORDER BY CREATED_AT DESC
        LIMIT {limit};
        """)
        return self.cur.fetchall()


class Message:

    author_id, content, flags, command_type = "", "", {}, UNKNOWN_COMMAND

