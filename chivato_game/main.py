from __future__ import annotations

import sqlite3

# Grupo 5 (aprobamos_pro): Saúl, Efrén y José Peña

DB_PATH = ':memory:'

con = sqlite3.connect(DB_PATH)
cur = con.cursor()
cur.execute("""CREATE TABLE game (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    my_decision BOOLEAN,
    other_decision BOOLEAN,
    my_score INTEGER,
    other_score INTEGER,
    my_total_score INTEGER,
    other_total_score INTEGER
    )
""")


def decision(other_decision: bool) -> bool:
    if other_decision is None:
        return None
    my_decision = False
    # Condición de inicialización de los registros.
    if cur.lastrowid < 1:
        cur.execute(
        """
    INSERT INTO game(id, my_decision, other_decision, my_score, other_score, my_total_score, other_total_score) VALUES (0,0,0,0,0,0,0)
    """
    )
    con.commit()
    if my_decision and other_decision:
        my_score, other_score = 3, 3
    elif my_decision and not other_decision:
        my_score, other_score = 0, 7
    # De la linea 34 a la 37 no haria falta ya que nuestra estrategia es no delatar 
    # nunca pero las ponemos para que se entiendan las posibles combinaciones.
    elif not my_decision and other_decision:
        my_score, other_score = 7, 0
    else:
        my_score, other_score = 1, 1
    
    current_score = cur.execute(f'SELECT my_total_score, other_total_score FROM game WHERE id={cur.lastrowid}')
    my_total_score, other_total_score = current_score.fetchone()
    my_total_score, other_total_score = my_total_score + my_score, other_total_score + other_score

    cur.execute(
        """
    INSERT INTO game(my_decision, other_decision, my_score, other_score, my_total_score, other_total_score) VALUES (?,?,?,?,?,?)
    """,
        (my_decision, other_decision, my_score, other_score, my_total_score, other_total_score),
    )
    con.commit()
    return my_score, other_score


# Caso de prueba 

# rounds = [False, False, True, False, True]

# for round in rounds:
#     points = decision(round)
#     print(f"""
#     RONDA {cur.lastrowid}:
#     Mis puntos: {points[0]}.
#     Sus puntos: {points[1]}.
#     """)

# print('\nHistorial de rondas:')
# for row in cur.execute('SELECT * FROM game'):
#     print(f'{row}')
# con.close()
