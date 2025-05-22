from __future__ import annotations

import sqlite3

DB_PATH = ':memory:'

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("""CREATE TABLE game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    my_decision BOOLEAN,
    rival_decision BOOLEAN,
    my_score INTEGER,
    rival_score INTEGER
    )
""")


def decision(my_decision: bool, rival_decision: bool):
    if my_decision and rival_decision:
        my_score, rival_score = 3, 3
    elif my_decision and not rival_decision:
        my_score, rival_score = 0, 7
    elif not my_decision and rival_decision:
        my_score, rival_score = 7, 0
    else:
        my_score, rival_score = 1, 1

    cur.execute(
        """
    INSERT INTO game(my_decision, rival_decision, my_score, rival_score) VALUES (?,?,?,?)
    """,
        (my_decision, rival_decision, my_score, rival_score),
    )
    con.commit()
    return my_score, rival_score


rounds = [(True, False), (False, False), (True, True), (True, False), (False, True)]

for round in rounds:
    points = decision(*round)
    print(f"""
    RONDA {round}:
    Yo {points[0]} puntos.
    Rival {points[1]} puntos.
    """)

print('\nHistorial de rondas:')
for row in cur.execute('SELECT * FROM game'):
    print(f'{row}')

con.close()
