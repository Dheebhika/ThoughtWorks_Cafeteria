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


# def post_data(connection, user_data):
#     cursor = connection.cursor()
#     cursor.execute("""insert into login_table(employee_id,username) values( %s, %s);""",
#                    (user_data['employee_id'], user_data['username']))
#     connection.commit()
#     cursor.close()


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id=%(id)s",
                   {'id': user_data['employee_id']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('login_page.html')
    else:
        # post_data(connection, user_data)
        return render_template('types_of_beverages.html')


@app.route('/beverages', methods=['POST'])
def post_data_request():
    return validate_data(connection, request.form)


# @app.route('/juice-world')
# def vendor_logins():
#     return render_template('hot_beverages_list.html')


@app.route('/vendor-login')
def vendor_login():
    return render_template('types_of_beverages.html')


@app.route('/juice-world')
def juice_world_login():
    return render_template("vendor_login.html", name='1001')


@app.route('/madras-cafe')
def madras_cafe_login():
    return render_template("vendor_login.html", name='1002')


@app.route('/vendor-type', methods=['POST'])
def vendor_operation():
    return validate_vendor(connection, request.form)


def validate_vendor(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select vendor_id,password from vendor_details where vendor_id=%(id)s AND password=%(password)s",
                   {'id': user_data['vendor_id'], 'password': user_data['pwd']}, )

    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('vendor_login.html')
    else:
        return render_template('vendor_type.html', vendorname=user_data['vendor_id'])


@app.route('/availability')
def hot():
    rows = database_connection(connection, request.query_string)
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("beverages_jinja.html", items=items)


def database_connection(connection, user_data):
    cursor = connection.cursor()
    query = "select name from beverage_details where vendor_id = %s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()
    return record


@app.route('/submission', methods=['POST'])
def menu_list():
    return database_connection_list(connection, request.form)


def database_connection_list(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    set_data_null = "update beverage_details set is_available=''"
    set_data = "update beverage_details set is_available = 'yes' WHERE name IN %s"
    cursor.execute(set_data_null)
    cursor.execute(set_data, (array,))
    connection.commit()
    cursor.close()


@app.route('/juice_world')
def cold_item():
    rows = display_available_cold_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("list_cold_beverages_jinja.html", items=items)


def display_available_cold_items():
    cursor = connection.cursor()
    cursor.execute("select name from beverage_details where is_available='yes'")
    record = cursor.fetchall()
    return record




if __name__ == '__main__':
    app.run(debug=True)
