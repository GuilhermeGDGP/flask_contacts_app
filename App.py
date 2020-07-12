from flask import Flask, render_template
from flask_mysqldb import MySQL

data = []
with open('configdb.txt') as load:
    for line in load:
        data.append(line.strip())

app = Flask(__name__)
app.config['MYSQL_HOST'] = data[0]
app.config['MYSQL_USER'] = data[1]
app.config['MYSQL_PASSWORD'] = data[2]
app.config['MYSQL_DB'] = data[3]
mysql = MySQL(app)

@app.route('/')
def Index():
    return render_template('index.html')

@app.route('/add_contact')
def add_contact():
    return 'add_contact'

@app.route('/edit')
def edit_contact():
    return 'edit_contact'

@app.route('/delete')
def delete_contact():
    return 'delete_contact'

if __name__ == '__main__':
    app.run(port=3000, debug=True)