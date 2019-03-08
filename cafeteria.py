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


@app.route('/employee-choice', methods=['POST'])
def post_data_request():
    return validate_data(connection, request.form)


def validate_data(connection, user_data):
    cursor = connection.cursor()
    cursor.execute("select employee_id from employee_details where employee_id=%(id)s",
                   {'id': user_data['employee_id']}, )
    returned_rows = cursor.fetchall()
    cursor.close()
    if len(returned_rows) == 0:
        return render_template('welcome_page.html')
    else:
        return render_template('types_of_beverages_employee.html', item=user_data['employee_id'])


@app.route('/beverages-for-cold', methods=['POST'])
def cold_all_items():
    return cold_item(connection, request.form)


def cold_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = display_available_cold_items()
    items = []
    for row in rows:
        items.append({"id": row[0], "name": row[1]})
    return render_template("list_cold_beverages_jinja.html", items=items, employee_id=array_value)


def display_available_cold_items():
    cursor = connection.cursor()
    cursor.execute("select item_id,name from beverage_details where is_available='yes' AND vendor_id=1001")
    record = cursor.fetchall()
    return record


@app.route('/beverages-for-hot', methods=['POST'])
def hot_all_items():
    return hot_item(connection, request.form)


def hot_item(connection, user_data):
    connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]
    rows = display_available_hot_items()
    items = []
    for row in rows:
        items.append({"id": row[0], "name": row[1]})
    return render_template("list_hot_beverages_jinja.html", item=items, employee_id=array_value)


def display_available_hot_items():
    cursor = connection.cursor()
    cursor.execute("select name from beverage_details where is_available  ='yes' AND vendor_id=1002")
    record = cursor.fetchall()

    return record


@app.route('/cold-item', methods=['POST'])
def update_item():
    update(connection, request.form)
    return render_template('welcome_page.html')


def update(connection, user_data):
    values = list(user_data.values())
    employee_value = values[0]
    values.remove(values[0])
    item_key = list(user_data.keys())
    item_key.remove(item_key[0])

    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) > 0:
            cursor = connection.cursor()
            update_details = "insert into ordered_items(item_id,employee_id,quantity) select item_id,{},{} from beverage_details where item_id = {}".format(
                employee_value, quantity, id)

            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            print(0)


@app.route('/hot-item', methods=['POST'])
def update_item_hot():
    update_hot(connection, request.form)
    return render_template('welcome_page.html')


def update_hot(connection, user_data):
    values = list(user_data.values())
    employee_value = values[0]
    values.remove(values[0])
    item_key = list(user_data.keys())
    item_key.remove(item_key[0])

    for id in list(item_key):
        quantity = user_data[id]
        if int(quantity) > 0:
            cursor = connection.cursor()
            update_details = "insert into ordered_items(item_id,employee_id,quantity) select item_id,{},{} from beverage_details where item_id = {}".format(
                employee_value, quantity, id)

            cursor.execute(update_details)
            connection.commit()
            cursor.close()
        else:
            print(0)


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
    return set_data


@app.route('/report_generation_button', methods=['POST'])
def calculation_for_report():
    sum = calculation(connection, request.form)
    cost = total(connection, request.form)
    sum_cost = tuple(sum)
    array = tuple(cost)

    return render_template("generate_report.html", item=array, items=sum_cost)


def calculation(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]

    sql_update = "select ordered_items.employee_id,beverage_details.item_id,ordered_items.date,sum(ordered_items.quantity*beverage_details.cost) FROM ordered_items inner join beverage_details on ordered_items.item_id=beverage_details.item_id GROUP BY ordered_items.employee_id,beverage_details.item_id,ordered_items.date ORDER BY employee_id"
    cursor.execute(sql_update, {'vendor_id': array_value})
    cost = cursor.fetchall()
    cursor.close()
    return cost


def total(connection, user_data):
    cursor = connection.cursor()
    array_values = tuple(user_data.values())
    array_value = array_values[0]

    sql_query = "select sum(quantity*cost) from beverage_details inner join ordered_items on beverage_details.item_id = ordered_items.item_id where vendor_id = %(id)s"
    cursor.execute(sql_query, {'id': array_value})
    total_cost = cursor.fetchall()
    cursor.close()
    return total_cost


if __name__ == '__main__':
    app.run(debug=True)
