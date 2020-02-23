import sqlite3
from sqlite3 import DatabaseError, Cursor
from sqlite3.dbapi2 import OperationalError

from utils import Defaults


def getConnection():
	conn = sqlite3.connect(Defaults.DB_PATH)
	createYandexTrackTable(conn)
	createLibTable(conn)
	return conn


def saveYandexTrack(c, t_id, title, artist, album):
	c.execute('INSERT INTO yandex_tracks VALUES (?, ?, ?, ?)', (t_id, title, artist, album))
	return t_id, title, artist, album


def getYandexTrack(c, t_id):
	c.execute('SELECT * FROM yandex_tracks WHERE id=?', (t_id,))
	return c.fetchone()


def createYandexTrackTable(conn):
	c = conn.cursor()
	try:
		c.execute("CREATE TABLE yandex_tracks (id text PRIMARY KEY, title text, artist text, album text)")
		conn.commit()
	except OperationalError as err:
		pass
	except DatabaseError as err:
		print("DB error", err)
		pass


def createLibTable(conn):
	c = conn.cursor()
	try:
		c.execute("CREATE TABLE tracks_lib (path text PRIMARY KEY, title text, artist text, album text)")
		conn.commit()
	except OperationalError:
		pass


def addLibEntry(c, path, title, artist, album):
	c.execute('INSERT INTO tracks_lib VALUES (?, ?, ?, ?)', (path, title, artist, album))
	return path, title, artist, album


def getLibEntry(c: Cursor, path: str):
	c.execute('SELECT * FROM tracks_lib WHERE path=?', (path,))
	return c.fetchone()


# TODO: Dev time thing. Remove it.
def getLibAll(c: Cursor):
	c.execute('SELECT * FROM tracks_lib')
	return c.fetchall()
