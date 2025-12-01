import sqlite3

connect = sqlite3.connect('movies.db')
cursor = connect.cursor()

cursor.execute("""
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER,
    type TEXT
)
""")

cursor.execute("""
CREATE TABLE actors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE movie_actors (
    movie_id INTEGER,
    actor_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES movies(id),
    FOREIGN KEY (actor_id) REFERENCES actors(id)
)
""")

movies_data = [
    (1, 'Криминальное чтиво', 1994, 'фильм'),
    (2, 'Бесславные ублюдки', 2009, 'фильм'),
    (3, 'Начало', 2010, 'фильм'),
    (4, 'Темный рыцарь', 2008, 'фильм'),
    (5, 'Друзья', 1994, 'сериал')
]

cursor.executemany("INSERT INTO movies VALUES (?, ?, ?, ?)", movies_data)

actors_data = [
    (1, 'Джон Траволта'),
    (2, 'Ума Турман'),
    (3, 'Сэмюэл Л. Джексон'),
    (4, 'Брэд Питт'),
    (5, 'Кристоф Вальц'),
    (6, 'Леонардо ДиКаприо'),
    (7, 'Джозеф Гордон-Левитт'),
    (8, 'Киллиан Мерфи'),
    (9, 'Майкл Кейн'),
    (10, 'Том Харди'),
    (11, 'Кристиан Бейл'),
    (12, 'Хит Леджер'),
    (13, 'Мэттью Перри'),
    (14, 'Дженнифер Энистон'),
    (15, 'Кортни Кокс')
]

cursor.executemany("INSERT INTO actors VALUES (?, ?)", actors_data)

movie_actors_data = [
    (1, 1), (1, 2), (1, 3),
    (2, 4), (2, 5),
    (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
    (4, 8), (4, 9), (4, 11), (4, 12),
    (5, 13), (5, 14), (5, 15)
]

cursor.executemany("INSERT INTO movie_actors VALUES (?, ?)", movie_actors_data)

connect.commit()

print("1. ФИЛЬМЫ БЕЗ АКТЕРОВ:")
cursor.execute("""
    SELECT movies.title
    FROM movies 
    LEFT JOIN movie_actors ON movies.id = movie_actors.movie_id
    WHERE movie_actors.actor_id IS NULL;
""")
for movie in cursor.fetchall():
    print(f"   {movie[0]}")
if not cursor.rowcount:
    print("   (все фильмы имеют актеров)")

print("\n2. АКТЕР В МАКСИМАЛЬНОМ КОЛИЧЕСТВЕ ФИЛЬМОВ:")
cursor.execute("""
    SELECT actors.name, COUNT(*) as film_count
    FROM actors
    INNER JOIN movie_actors ON actors.id = movie_actors.actor_id
    GROUP BY actors.id
    ORDER BY film_count DESC
    LIMIT 3;
""")
for actor in cursor.fetchall():
    print(f"   {actor[0]} - {actor[1]} фильма")

print("\n3. АКТЕРЫ С БОЛЕЕ ЧЕМ 1 ФИЛЬМОМ:")
cursor.execute("""
    SELECT actors.name, COUNT(*) as film_count
    FROM actors
    INNER JOIN movie_actors ON actors.id = movie_actors.actor_id
    GROUP BY actors.id
    HAVING film_count > 1
    ORDER BY film_count DESC;
""")
for actor in cursor.fetchall():
    print(f"   {actor[0]} ({actor[1]} фильма)")

print("\n4. ВСЕ ФИЛЬМЫ С АКТЕРАМИ:")
cursor.execute("""
    SELECT movies.title, actors.name
    FROM movies
    INNER JOIN movie_actors ON movies.id = movie_actors.movie_id
    INNER JOIN actors ON movie_actors.actor_id = actors.id
    ORDER BY movies.title, actors.name;
""")

current_movie = ""
for movie, actor in cursor.fetchall():
    if movie != current_movie:
        print(f"\n   {movie}:")
        current_movie = movie
    print(f"      {actor}")

connect.close()