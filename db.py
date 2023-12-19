import sqlite3
from pathlib import Path
 
import click
from flask import g, current_app, jsonify

 
 
DATABASE = './TischResDB.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))
 
    db.row_factory = make_dicts
    return db
 

        
 
def init_db(app):
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
    with app.app_context():
        db = get_db()
        with app.open_resource('bookingsystem.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
 
 
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
 
