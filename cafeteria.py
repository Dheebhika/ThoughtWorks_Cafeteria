import psycopg2
from flask import Flask, request, render_template
from flask_cors import CORS

# from post_data_to_database import post_data

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
    employee_id = cursor.execute("""select employee_id from employee_details where employee_id=%s ;""", (user_data['employee_id'],))
    if employee_id == user_data['employee_id']:
        return render_template('types_of_beverages.html')
    else:
        return render_template('login_page.html')
    connection.commit()
    cursor.close()


@app.route('/types_of_beverages', methods=['POST'])
def post_data_request():
    validate_data(connection, request.form)
    return render_template('types_of_beverages.html', shared=request.form)


if __name__ == '__main__':
    app.run()
