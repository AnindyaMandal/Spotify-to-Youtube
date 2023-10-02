import sqlite3, os



db_file = 'song_data.db'

def create_db():
    if (os.path.exists(db_file)):
        print("Database already exists by the name:", db_file)
    else:
        print(db_file, " Does not exist. \n...Creating DB...\n\tID (int prim key)\n\tsong_name (text)\n\tartists (text)\n\tquery(text)\n\turl(text)")
        conn = sqlite3.connect('song_data.db')

        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS liked_songs (
                id INTEGER PRIMARY KEY,
                song_name TEXT,
                artists TEXT,
                album_name TEXT,
                query TEXT,
                url TEXT
            )
        ''')
        print("Created DB: " + str(db_file))

def search_by_name(name):
    pass

def insert_song(name, artists, album, url):
    pass

def remove_song(name, artists, album, url):
    pass


