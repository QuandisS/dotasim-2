import sqlite3

bd = sqlite3.connect('../data/data.db')
cursor = bd.cursor()



cursor.close()
bd.close()