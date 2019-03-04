import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
connection = psycopg2.connect("dbname = thoughtworks_cafeteria user=admin")


@app.route('/')
def login_page():
    return render_template('welcome_page.html')


@app.route('/employee-login')
def employee_page():
    return render_template('employee_page.html')


@app.route('/beverages', methods=['POST'])
def post_data_request():
    return validate_data(connection, request.form)


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id=%(id)s",
                   {'id': user_data['employee_id']})
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        # post_data(connection, user_data)
        return render_template('types_of_beverages_employee.html')


@app.route('/employee-choice')
def employee_choice():
    return render_template('types_of_beverages_employee.html')


# def post_data(connection, user_data):
#     cursor = connection.cursor()
#     cursor.execute("""insert into login_table(employee_id,username) values( %s, %s);""",
#                    (user_data['employee_id'], user_data['username']))
#     connection.commit()
#     cursor.close()


@app.route('/beverages-for-cold')
def cold_item():
    rows = display_available_cold_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("list_cold_beverages_jinja.html", items=items)


def display_available_cold_items():
    cursor = connection.cursor()
    cursor.execute("select name from beverage_details where is_available='yes' AND vendor_id=1001")
    record = cursor.fetchall()
    return record


@app.route('/beverages-for-hot')
def hot_items():
    rows = database_selected_hot_items()
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("list_hot_beverages_jinja.html", items=items)


def database_selected_hot_items():
    cursor = connection.cursor()
    cursor.execute("select name from beverage_details where is_available  ='yes' AND vendor_id=1002 ")
    record = cursor.fetchall()

    return record


@app.route('/vendor-login')
def vendor_login():
    return render_template('types_of_beverages_vendor.html')


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
        return render_template('vendor_type.html', vendorname=user_data['vendorname'])


@app.route('/availability')
def hot():
    rows = database_connection(connection, request.query_string)
    returned = (int(request.query_string.decode().split('=')[1]),)
    lists = list(returned)
    index = lists[0]
    items = []
    for row in rows:
        items.append(row[0])
    return render_template("beverages_jinja.html", items=items, name=index)


def database_connection(connection, user_data):
    cursor = connection.cursor()
    query = "select name from beverage_details where vendor_id = %s;"
    cursor.execute(query, (int(user_data.decode().split('=')[1]),))
    record = cursor.fetchall()

    return record


@app.route('/submission', methods=['POST'])
def menu_list():
    row = database_connection_list(connection, request.form)
    return render_template('welcome_page.html', item=row)


def database_connection_list(connection, user_data):
    cursor = connection.cursor()
    array = tuple(user_data.keys())
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    set_data_null = "update beverage_details set is_available='' WHERE vendor_id=%(vendor_id)s"
    set_data = "update beverage_details set is_available = 'yes' WHERE name IN %s"
    cursor.execute(set_data_null, {'vendor_id': array_value})
    cursor.execute(set_data, (array,))
    connection.commit()
    cursor.close()


if __name__ == '__main__':
    app.run(debug=True)
