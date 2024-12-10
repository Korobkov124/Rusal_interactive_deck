import sqlite3

def connect_db():
    try:
        connection = sqlite3.connect("maindb.db")
        print("Connection successful")
        return connection
    except sqlite3.Error as error:
        print("Failed to connect database", error)
        return None

def query_db(name_table):
    conn = connect_db()
    data = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM{name_table}")
            rows = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            for row in rows:
                row_dict = dict(zip(column_names, row))
                data.append(row_dict)
        except sqlite3.Error as error:
            print("Failed to connect database", error)
    conn.close()
    return data

if __name__ == "__main__":
    data_user = query_db(" booking")
    print(data_user)