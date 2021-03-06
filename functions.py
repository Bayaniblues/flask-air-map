import sqlite3
import pandas as pd
import json


# Higher order functions to filter database queries
def coordinate_matrix():
    con = sqlite3.connect('db.sqlite3')
    df2 = pd.read_sql_query("SELECT lon FROM record WHERE parameter='pm25'", con)
    df1 = pd.read_sql_query("SELECT lat FROM record WHERE parameter='pm25'", con)

    state = []
    for i, (x, y) in enumerate(zip(df1.values, df2.values)):
        state.append([x[0],y[0]])
    #print(state)
    con.close()
    return json.dumps(state)


def get_lat_array():
    con = sqlite3.connect('db.sqlite3')
    #df2 = pd.read_sql_query("SELECT lon FROM record WHERE parameter='pm25'", con)
    df1 = pd.read_sql_query("SELECT lat FROM record WHERE parameter='pm25'", con)
    con.close()
    state = []
    for i, x in enumerate(df1.values):
        state.append(x[0])
    return state

def get_long_array():
    con = sqlite3.connect('db.sqlite3')
    df1 = pd.read_sql_query("SELECT lon FROM record WHERE parameter='pm25'", con)
    #df1 = pd.read_sql_query("SELECT lat FROM record WHERE parameter='pm25'", con)
    con.close()
    state = []
    for i, x in enumerate(df1.values):
        state.append(x[0])

    return state


def search_city(input_city):
    con = sqlite3.connect('db.sqlite3')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(f"SELECT * FROM record \
                WHERE city='{input_city}' \
                GROUP BY city;")
    rows = cur.fetchall()
    return rows


def unique_cities():
    con = sqlite3.connect('db.sqlite3')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT DISTINCT city FROM record \
                GROUP BY city;")
    rows = cur.fetchall()
    return rows
