# database.py
# ============================================
# Работа с SQLite базой данных
# ============================================

import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

def ensure_db_directory():
    """Создает директорию для базы данных, если её нет"""
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

def init_database():
    """Инициализация базы данных SQLite"""
    ensure_db_directory()
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Таблица пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP
        )
    ''')
    
    # Таблица для логов действий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT,
            event_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
    ''')
    
    # Таблица мероприятий для подбора
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            budget INTEGER NOT NULL,
            vibe TEXT NOT NULL,
            time TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Таблица еженедельных событий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weekly_events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    # Таблица случайных событий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS random_events (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            description TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")

# ====== РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ======

def add_user(user_id, name, age, phone):
    """Добавляет нового пользователя в базу"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT OR REPLACE INTO users (user_id, name, age, phone, last_activity)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, age, phone, datetime.now()))
        conn.commit()
        return True
    except Exception as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False
    finally:
        conn.close()

def get_user(user_id):
    """Получает данные пользователя из БД"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return {
            "user_id": user[0],
            "name": user[1],
            "age": user[2],
            "phone": user[3],
            "registered_at": user[4],
            "last_activity": user[5]
        }
    return None

def update_user_activity(user_id):
    """Обновляет время последней активности пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users SET last_activity = ? WHERE user_id = ?
    ''', (datetime.now(), user_id))
    
    conn.commit()
    conn.close()

def log_action(user_id, action, event_id=None):
    """Логирует действия пользователя"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO user_actions (user_id, action, event_id)
        VALUES (?, ?, ?)
    ''', (user_id, action, event_id))
    
    conn.commit()
    conn.close()

# ====== РАБОТА С МЕРОПРИЯТИЯМИ ======

def get_filtered_events(budget=None, category=None, vibe=None, time=None):
    """Получает события из БД с фильтрацией"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM events WHERE 1=1"
    params = []
    
    if budget is not None:
        query += " AND budget <= ?"
        params.append(budget)
    if category:
        query += " AND category = ?"
        params.append(category)
    if vibe:
        query += " AND vibe = ?"
        params.append(vibe)
    if time:
        query += " AND time = ?"
        params.append(time)
    
    cursor.execute(query, params)
    events = cursor.fetchall()
    conn.close()
    
    result = []
    for e in events:
        result.append({
            "id": e[0],
            "title": e[1],
            "category": e[2],
            "budget": e[3],
            "vibe": e[4],
            "time": e[5],
            "url": e[6],
            "description": e[7]
        })
    return result

def get_random_filtered_event(budget, category, vibe, time):
    """Случайное событие из БД по параметрам"""
    events = get_filtered_events(budget, category, vibe, time)
    import random
    return random.choice(events) if events else None

def get_random_weekly_event():
    """Случайное еженедельное событие"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weekly_events ORDER BY RANDOM() LIMIT 1")
    event = cursor.fetchone()
    conn.close()
    
    if event:
        return {
            "title": event[1],
            "date": event[2],
            "url": event[3],
            "description": event[4]
        }
    return None

def get_random_event():
    """Абсолютно случайное событие"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM random_events ORDER BY RANDOM() LIMIT 1")
    event = cursor.fetchone()
    conn.close()
    
    if event:
        return {
            "title": event[1],
            "url": event[2],
            "description": event[3]
        }
    return None

# ====== ЗАПОЛНЕНИЕ ТЕСТОВЫМИ ДАННЫМИ ======

def fill_test_data():
    """Заполняет базу тестовыми данными"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Очищаем таблицы
    cursor.execute("DELETE FROM events")
    cursor.execute("DELETE FROM weekly_events")
    cursor.execute("DELETE FROM random_events")
    
    # События для подбора
    events = [
        # Кино
        (1, "🍿 'Дюна: Часть вторая' в IMAX", "кино", 800, "спокойная", "вечер", 
         "https://afisha.ru/movie/dune2", "Эпическое продолжение в формате IMAX."),
        (2, "🍿 Премьера: 'Мастер и Маргарита'", "кино", 500, "спокойная", "день", 
         "https://afisha.ru/movie/master", "Новая экранизация культового романа."),
        (3, "🍿 Ночной показ: 'Брат 2'", "кино", 400, "активная", "вечер", 
         "https://afisha.ru/movie/brat2", "Культовое кино под пиво."),
        
        # Театр
        (4, "🎭 Спектакль '№13D'", "театр", 3000, "активная", "вечер", 
         "https://theatre.ru/13d", "Комедия положений с любимыми актерами."),
        (5, "🎭 Балет 'Лебединое озеро'", "театр", 5000, "спокойная", "вечер", 
         "https://bolshoi.ru/swan", "Легендарный балет Большого театра."),
        
        # Выставки
        (6, "🖼️ Выставка 'Босх и Брейгель'", "выставка", 600, "спокойная", "день", 
         "https://pushkinmuseum.ru/bosch", "Редкие работы северных мастеров."),
        (7, "🖼️ Мультимедийная выставка 'Ван Гог'", "выставка", 800, "спокойная", "вечер", 
         "https://vangogh.ru", "Погружение в мир художника."),
        
        # Мастер-классы
        (8, "🍳 Мастер-класс итальянской кухни", "мастер-классы", 3500, "спокойная", "день", 
         "https://chef.ru/pasta", "Готовим пасту и тирамису с шефом."),
        (9, "🎨 Мастер-класс по рисованию", "мастер-классы", 2000, "спокойная", "вечер", 
         "https://artstudio.ru/night", "Нарисуй шедевр с бокалом вина."),
        
        # Вечеринки
        (10, "🎉 Вечеринка '90-е'", "вечеринки", 1500, "активная", "вечер", 
         "https://clubrai.ru/90s", "Руки Вверх и танцы до утра."),
        (11, "🎉 Afterwork в баре", "вечеринки", 2000, "активная", "вечер", 
         "https://strelka.ru/afterwork", "Коктейли и диджей."),
        
        # Концерты
        (12, "🤘 Концерт 'Король и Шут'", "концерты", 3000, "активная", "вечер", 
         "https://kingandjester.ru", "Панк-рок в честь 35-летия."),
        (13, "🎹 Концерт джазовой музыки", "концерты", 2000, "спокойная", "вечер", 
         "https://jazz.ru/evening", "Уютный вечер с живым джазом."),
    ]
    
    cursor.executemany('''
        INSERT INTO events (id, title, category, budget, vibe, time, url, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', events)
    
    # Еженедельные события
    weekly = [
        (1, "🍔 Фестиваль 'Московское варенье'", "12-18 августа", 
         "https://mos.ru/festival/jam", "Дегустация варенья со всей России."),
        (2, "🎨 Ночь музеев в Москве", "15 августа", 
         "https://night.museums.ru", "Музеи работают бесплатно всю ночь."),
        (3, "⚽ Спартак - ЦСКА", "16 августа, 19:00", 
         "https://rpl.ru/spartak-cska", "Главное дерби страны."),
    ]
    
    cursor.executemany('''
        INSERT INTO weekly_events (id, title, date, url, description)
        VALUES (?, ?, ?, ?, ?)
    ''', weekly)
    
    # Случайные события
    random_events = [
        (1, "🎪 Цирк на Цветном бульваре", "https://circus.ru", 
         "Новая программа 'Вокруг света'."),
        (2, "🚤 Прогулка на теплоходе", "https://riverboat.ru", 
         "Романтическая прогулка с музыкой."),
        (3, "🎤 Стендап концерт", "https://standup.ru/guram", 
         "Новая программа 'Неформат'."),
        (4, "🧘 Медитация в саду", "https://meditation.ru/garden", 
         "Групповая медитация на воздухе."),
        (5, "🎲 Настольные игры", "https://antikafe.ru/cell", 
         "100 настолок, чай и печеньки."),
    ]
    
    cursor.executemany('''
        INSERT INTO random_events (id, title, url, description)
        VALUES (?, ?, ?, ?)
    ''', random_events)
    
    conn.commit()
    conn.close()
    print("✅ Тестовые данные загружены")

# Инициализируем БД при импорте
init_database()