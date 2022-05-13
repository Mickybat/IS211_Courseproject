import sqlite3

Blog_TABLE = """ 
CREATE TABLE IF NOT EXISTS posts( 
    post_id integer PRIMARY KEY AUTOINCREMENT, 
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL, 
    content TEXT NOT NULL,  
    author TEXT NOT  NULL
)
"""


def create_tables():
    conn = sqlite3.connect('blog.db')

    cur = conn.cursor()
    cur.execute(Blog_TABLE)
    conn.commit()

    conn.close()


if __name__ == "__main__":
    create_tables()