import sqlite3
import random

conn = sqlite3.connect("events.db")
cursor = conn.cursor()


def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        phone TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        place TEXT,
        atmosphere TEXT,
        time TEXT,
        budget INTEGER,
        link TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS city_events(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        link TEXT
    )
    """)

    conn.commit()


def add_user(name, age, phone):
    cursor.execute(
        "INSERT INTO users(name, age, phone) VALUES(?,?,?)",
        (name, age, phone)
    )
    conn.commit()


def find_event(place, atmosphere, time, budget):

    cursor.execute("""
    SELECT * FROM events
    WHERE place=? AND atmosphere=? AND time=? AND budget<=?
    """, (place, atmosphere, time, budget))

    events = cursor.fetchall()

    if events:
        return random.choice(events)

    return None


def random_event():

    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()

    return random.choice(events)


def city_events():

    cursor.execute("SELECT * FROM city_events")
    return cursor.fetchall()