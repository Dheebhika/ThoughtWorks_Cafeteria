import psycopg2
from flask import Flask, render_template, request
from cafeteria import connection

app = Flask(__name__)


@app.route('/')
def hot():
    rows = database_connection_hot()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("hot_beverages_jinja.html", items=items)


@app.route('/submission', methods=['POST'])
def menu_list_hot():
    return database_connection_list_hot(connection, request.form)


def database_connection_list_hot(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    set_data = "update hot_beverages set availabilty = 'yes' WHERE items  IN %s"
    cursor.execute(set_data, (array,))
    connection.commit()
    cursor.close()


def database_connection_hot():
    connection = psycopg2.connect(user="admin", host="127.0.0.1", port="5432",
                                  database="thoughtworks_cafeteria")
    cursor = connection.cursor()
    cursor.execute("select items from hot_beverages")
    record = cursor.fetchall()

    return record


if __name__ == '__main__':
    app.run()
