import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = thoughtworks_cafeteria user=admin")


@app.route('/')
def login_page():
    return render_template('login_page.html')


@app.route('/employee-login')
def employee_page():
    return render_template('employee_page.html')


def post_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("""insert into login_table(employee_id,username) values( %s, %s);""",
                   (user_data['employee_id'], user_data['username']))
    connection.commit()
    cursor.close()


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id=%(id)s",
                   {'id': user_data['employee_id']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('login_page.html')
    else:
        post_data(connection, user_data)
        return render_template('types_of_beverages.html')


@app.route('/types_of_beverages', methods=['POST'])
def post_data_request():
    return validate_data(connection, request.form)


@app.route('/vendor-login')
def vendor_login():
    return render_template('vendor_login.html')


def validate_vendor_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id from vendor_login where vendor_id=%(id)s",
                   {'id': user_data['vendor_id']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('login_page.html')
    else:
        return render_template('vendor_type.html')


@app.route('/vendor-type', methods=['POST'])
def post_data_request1():
    return validate_vendor_data(connection, request.form)


@app.route('/vendor')
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
    set_data_null = "update hot_beverages set check_availability=''"
    set_data = "update hot_beverages set check_availability = 'yes' WHERE items  IN %s"
    cursor.execute(set_data_null)
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
    app.run(debug=True)
