from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

data = []
with open('config.txt') as load:
    for line in load:
        data.append(line.strip())

app.config['MYSQL_HOST'] = data[0]
app.config['MYSQL_USER'] = data[1]
app.config['MYSQL_PASSWORD'] = data[2]
app.config['MYSQL_DB'] = data[3]
mysql = MySQL(app)

app.secret_key = data[4]

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    datadb = cur.fetchall()
    return render_template('index.html', contacts=datadb)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f'INSERT INTO contacts (name, phone, email) VALUES ("{name}", "{phone}", "{email}")')
        mysql.connection.commit()
        flash('Contact Added Successfully')
        return redirect(url_for('Index'))

@app.route('/edit/<string:id>')
def edit_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'SELECT * FROM contacts WHERE id = {id}')
    datadb = cur.fetchall()
    return render_template('edit-contact.html', contact=datadb[0])


@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute(f'UPDATE contacts SET name = "{name}", email = "{email}", phone = "{phone}" WHERE id = {id}')
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f'DELETE FROM contacts WHERE id = {id}')
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=3000, debug=True)