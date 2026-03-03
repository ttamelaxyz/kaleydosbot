#временная база данных в памяти для простоты
# лучше использовать SQLite/PostgreSQL

# Хранилище пользователей
users_db = {}

# База данных мероприятий
events_db = [
    # Кино
    {
        'id': 1,
        'title': 'Дюна: Часть вторая',
        'type': 'кино',
        'city': 'Москва',
        'description': 'Фантастический блокбастер в IMAX',
        'company': ['один', 'пара', 'друзья']
    },
    {
        'id': 2,
        'title': 'Мастер и Маргарита',
        'type': 'кино',
        'city': 'Москва',
        'description': 'Новая экранизация романа Булгакова',
        'company': ['один', 'пара', 'друзья']
    },
    
    # Концерты
    {
        'id': 3,
        'title': 'Концерт группы "Звери"',
        'type': 'концерт',
        'city': 'Москва',
        'description': 'Живой звук, любимые хиты',
        'company': ['один', 'пара', 'друзья']
    },
    {
        'id': 4,
        'title': 'Классика в темноте',
        'type': 'концерт',
        'city': 'Москва',
        'description': 'Концерт симфонической музыки при свечах',
        'company': ['пара', 'один']
    },
    
    # Выставки
    {
        'id': 5,
        'title': 'Импрессионисты',
        'type': 'выставка',
        'city': 'Москва',
        'description': 'Выставка картин Мане, Моне, Ренуара',
        'company': ['один', 'пара', 'друзья']
    },
    {
        'id': 6,
        'title': 'Роботы и трансформеры',
        'type': 'выставка',
        'city': 'Москва',
        'description': 'Интерактивная выставка для детей и взрослых',
        'company': ['друзья', 'семья']
    },
    
    # Театр
    {
        'id': 7,
        'title': 'Гамлет',
        'type': 'театр',
        'city': 'Москва',
        'description': 'Трагедия Шекспира в постановке театра на Таганке',
        'company': ['один', 'пара']
    },
    {
        'id': 8,
        'title': 'Собачье сердце',
        'type': 'театр',
        'city': 'Москва',
        'description': 'Спектакль по повести Булгакова',
        'company': ['пара', 'друзья']
    },
    
    # Спектакли для компании
    {
        'id': 9,
        'title': 'Квиз "Мозгобойня"',
        'type': 'квиз',
        'city': 'Москва',
        'description': 'Интеллектуальная командная игра в баре',
        'company': ['друзья']
    },
    {
        'id': 10,
        'title': 'Антикафе "Циферблат"',
        'type': 'анти-кафе',
        'city': 'Москва',
        'description': 'Место для игр и общения с друзьями',
        'company': ['друзья']
    }
]

def get_user(user_id):
    """Получить пользователя по ID"""
    return users_db.get(user_id)

def save_user(user_id, user_data):
    """Сохранить пользователя"""
    users_db[user_id] = user_data

def get_events_by_preferences(city, event_type=None, company=None):
    """Получить события по предпочтениям"""
    filtered_events = []
    
    for event in events_db:
        # Проверяем город
        if event['city'].lower() != city.lower():
            continue
        
        # Проверяем тип события (если указан)
        if event_type and event['type'] != event_type:
            continue
        
        # Проверяем компанию (если указана)
        if company and company not in event['company']:
            continue
        
        filtered_events.append(event)
    
    return filtered_events

def get_event_types():
    """Получить все типы событий"""
    types = set()
    for event in events_db:
        types.add(event['type'])
    return sorted(list(types))