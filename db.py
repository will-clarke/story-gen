import sqlite3
import uuid
import random

connection = sqlite3.connect("stories.db")

cursor = connection.cursor()


def setup():
    cursor.execute( """
    CREATE TABLE IF NOT EXISTS stories (
        id TEXT PRIMARY KEY,
        text TEXT,
        prompt TEXT,
        update_at datetime,
        created_at datetime
    )
    """)

    cursor.execute( """
    CREATE TABLE IF NOT EXISTS story_categories (
        id TEXT,
        category TEXT,
        value TEXT,

        FOREIGN KEY(id) REFERENCES story(id)
    )
    """)

def close():
    connection.commit()
    connection.close()

def load_fake_data():
    u   = str(uuid.uuid4())
    cursor.execute("INSERT INTO stories VALUES ('%s', 'This is an answer', 'write a question', DATE('now'), DATE('now'))" %(u))

    potential_genres = ["historical", "fantasy", "romantic", "suspense", "sci-fi", "noir", "adventure", "comedy", "mystery", "fantasy", "romance"]
    potential_tones = ["eerie", "suspense", "joyful", "celebration", "melancholic", "reflective", "funny", "comedy", "tense"]

    for _ in range(0, random.randint(1, 5)):
        cursor.execute("INSERT INTO story_categories VALUES ('%s', 'genre', '%s' )" %(u, random.choice(potential_genres)))
    for _ in range(0, random.randint(1, 5)):
        cursor.execute("INSERT INTO story_categories VALUES ('%s', 'tone', '%s' )" %(u, random.choice(potential_tones)))


    connection.commit()
