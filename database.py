import sqlite3
import random

conn = sqlite3.connect("events.db")
cursor = conn.cursor()


def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tg_id INTEGER UNIQUE,
        name TEXT,
        age INTEGER,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        place TEXT,
        atmosphere TEXT,
        time TEXT,
        budget INTEGER,
        link TEXT,
        image TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS city_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        image TEXT,
        link TEXT
    )
    """)

    conn.commit()

def city_events():

    cursor.execute("SELECT * FROM city_events")

    return cursor.fetchall()

def user_exists(tg_id):

    cursor.execute(
        "SELECT * FROM users WHERE tg_id=?",
        (tg_id,)
    )

    return cursor.fetchone()


def add_user(tg_id, name, age, phone):

    cursor.execute(
        "INSERT INTO users(tg_id,name,gender,phone) VALUES(?,?,?,?)",
        (tg_id, name, age, phone)
    )

    conn.commit()


def add_event(name, description, place, atmosphere, time, budget, link, image):

    cursor.execute("""
    INSERT INTO events(name,description,place,atmosphere,time,budget,link,image)
    VALUES(?,?,?,?,?,?,?,?)
    """, (name, description, place, atmosphere, time, budget, link, image))

    conn.commit()


def find_events(place, atmosphere, time, budget):

    cursor.execute("""
    SELECT * FROM events
    WHERE place=? AND atmosphere=? AND time=? AND budget<=?
    """, (place, atmosphere, time, budget))

    return cursor.fetchall()


def random_event():

    cursor.execute("SELECT * FROM events")

    events = cursor.fetchall()

    if not events:
        return None

    return random.choice(events)